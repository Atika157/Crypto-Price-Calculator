# 🪙 Crypto Price Calculator

A Python CLI tool that fetches real-time cryptocurrency prices 💹 and calculates your holdings' value 💰.
Supports **thousands** of coins by accepting **name**, **symbol**, or **CoinGecko ID** (e.g., `BTC`, `Bitcoin`, `bitcoin`).
Includes a **fallback API** to ensure reliability.

---

### 📺 Video Demo:
<https://youtu.be/wICHj2TTspc>

---

## ✨ Features
- 🔍 Search by **symbol**, **name**, or **CoinGecko ID**
- 🌐 Real-time prices from **CoinGecko** with **CoinCap** fallback
- 🛡 Validates user input for accuracy
- 🦖 Fun CLI output with `cowsay` 🐄
- ⚡ Fast & reliable (works with thousands of coins)

---

## 📦 Installation

1. **Clone this repository**
   git clone https://github.com/Atika157/Crypto-Price-Calculator
   cd crypto-price-calculator

## Install dependencies
pip install -r requirements.txt

## 🚀 Usage
Run the script like this:
python project.py <crypto_id_or_symbol_or_name> <amount>

# Examples:
python project.py btc 2,
python project.py ethereum 1.5,
python project.py dogecoin 1000,
python project.py shiba-inu 5000000,

## 🌟 Sample Output
 _____________
< 0.5 bitcoin = $32,456.78 >
 -------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||


## Files
1. **`project.py`** - Main application with 4 core functions:
   - `fetch_crypto_price()`: Gets prices from APIs with fallback logic
   - `calculate_value()`: Computes portfolio value with validation
   - `validate_input()`: Ensures proper number formatting
   - `main()`: Orchestrates the workflow

2. **`test_project.py`** - Contains pytest cases for:
   - Input validation (regex patterns)
   - Price calculation logic
   - Error handling

3. **`requirements.txt`** - Lists dependencies:
## Installation

pip install -r requirements.txt

## Design Choices
1. **Dual-API Architecture**:
- Uses CoinCap as primary and CoinGecko as fallback
- Ensures uptime if one API fails

2. **Input Validation**:
- Strict regex (`^[+]?\d*\.?\d+$`) prevents:
  - Negative numbers
  - Multiple decimals
  - Non-numeric input

3. **User Experience**:
- Uses `cowsay` for visual appeal
- Formatted output (e.g., `$42,069.42`)
- Clear error messages

### 📦 Project Structure
.
├── project.py          # Main application
├── test_project.py     # Test cases (pytest)
├── requirements.txt    # Dependencies
└── README.md           # Documentation

 🔒 Disclaimer
This tool is for educational purposes only.
Cryptocurrency prices are volatile 📉📈 — use responsibly.

❤️ Contributing
PRs are welcome!
Fork it, make changes, and submit a pull request 🚀.
