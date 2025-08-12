import sys
import requests
import re
import cowsay
from requests.exceptions import RequestException

COINGECKO_LIST_URL = "https://api.coingecko.com/api/v3/coins/list"

def get_coin_id(user_input):
    """Match user input (symbol, name, or ID) to a valid CoinGecko ID."""
    try:
        coins = requests.get(COINGECKO_LIST_URL, timeout=10).json()
        user_input = user_input.lower()

        # Exact ID match
        for coin in coins:
            if coin["id"] == user_input:
                return coin["id"]

        # Symbol match
        for coin in coins:
            if coin["symbol"] == user_input:
                return coin["id"]

        # Name match
        for coin in coins:
            if coin["name"].lower() == user_input:
                return coin["id"]

        sys.exit(f"Error: Cryptocurrency '{user_input}' not found. Check spelling or try full name.")
    except RequestException:
        sys.exit("Error: Could not fetch coin list from CoinGecko.")

def fetch_crypto_price(coin_id):
    """Fetch cryptocurrency price from CoinGecko with CoinCap fallback."""
    apis = [
        {
            "name": "CoinGecko",
            "url": f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd",
            "parse": lambda data: float(data[coin_id]["usd"])
        },
        {
            "name": "CoinCap",
            "url": f"https://api.coincap.io/v2/assets/{coin_id}",
            "parse": lambda data: float(data["data"]["priceUsd"])
        }
    ]

    for api in apis:
        try:
            response = requests.get(api["url"], timeout=10)
            response.raise_for_status()
            return api["parse"](response.json())
        except (RequestException, KeyError, ValueError):
            continue

    sys.exit(f"Error: Couldn't fetch price for '{coin_id}'.")

def calculate_value(amount, price):
    """Calculate and validate portfolio value."""
    if price <= 0:
        sys.exit("Error: Invalid price data received.")
    return round(amount * price, 2)

def validate_input(input_str):
    """Validate numeric amount."""
    return bool(re.match(r"^[+]?\d*\.?\d+$", input_str))

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python project.py <crypto_id_or_symbol_or_name> <amount>\nExample: python project.py btc 5")

    user_input, amount = sys.argv[1], sys.argv[2]

    if not validate_input(amount):
        sys.exit("Invalid amount. Use positive numbers only (e.g., 1.5 or 100).")

    coin_id = get_coin_id(user_input)
    price = fetch_crypto_price(coin_id)
    value = calculate_value(float(amount), price)
    cowsay.trex(f"{amount} {user_input.upper()} = ${value:,.2f}")

if __name__ == "__main__":
    main()
