import pytest
from unittest.mock import patch, MagicMock
import project  # your main file name

# ---------------------------
# Test validate_input
# ---------------------------
@pytest.mark.parametrize("value,expected", [
    ("10", True),
    ("10.5", True),
    ("0.0001", True),
    ("-5", False),
    ("abc", False),
    ("", False),
])
def test_validate_input(value, expected):
    assert project.validate_input(value) == expected

# ---------------------------
# Test calculate_value
# ---------------------------
def test_calculate_value_valid():
    assert project.calculate_value(2, 100) == 200.00

def test_calculate_value_invalid_price():
    with pytest.raises(SystemExit):
        project.calculate_value(2, 0)

# ---------------------------
# Test get_coin_id with mocked CoinGecko list
# ---------------------------
@patch("requests.get")
def test_get_coin_id_exact_id(mock_get):
    mock_get.return_value.json.return_value = [
        {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"},
        {"id": "ethereum", "symbol": "eth", "name": "Ethereum"}
    ]
    coin_id = project.get_coin_id("bitcoin")
    assert coin_id == "bitcoin"

@patch("requests.get")
def test_get_coin_id_symbol_match(mock_get):
    mock_get.return_value.json.return_value = [
        {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"}
    ]
    assert project.get_coin_id("btc") == "bitcoin"

@patch("requests.get")
def test_get_coin_id_name_match(mock_get):
    mock_get.return_value.json.return_value = [
        {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"}
    ]
    assert project.get_coin_id("Bitcoin") == "bitcoin"

@patch("requests.get")
def test_get_coin_id_not_found(mock_get):
    mock_get.return_value.json.return_value = []
    with pytest.raises(SystemExit):
        project.get_coin_id("unknowncoin")

# ---------------------------
# Test fetch_crypto_price with mocks
# ---------------------------
@patch("requests.get")
def test_fetch_crypto_price_from_coingecko(mock_get):
    # First API (CoinGecko) returns success
    mock_get.return_value.json.return_value = {"bitcoin": {"usd": 50000}}
    mock_get.return_value.raise_for_status = lambda: None
    price = project.fetch_crypto_price("bitcoin")
    assert price == 50000.0

@patch("requests.get")
def test_fetch_crypto_price_fallback_to_coincap(mock_get):
    # First API fails (CoinGecko)
    def side_effect(url, timeout):
        mock_response = MagicMock()
        mock_response.raise_for_status = lambda: None
        if "coingecko" in url:
            raise project.RequestException("API fail")
        else:
            mock_response.json.return_value = {"data": {"priceUsd": "3000"}}
        return mock_response

    mock_get.side_effect = side_effect
    price = project.fetch_crypto_price("ethereum")
    assert price == 3000.0

@patch("requests.get")
def test_fetch_crypto_price_failure(mock_get):
    # Both APIs fail
    mock_get.side_effect = project.RequestException("fail")
    with pytest.raises(SystemExit):
        project.fetch_crypto_price("unknown")
