
# Trading Bot

This trading bot is built using the Lumibot framework and Alpaca for trading operations, leveraging sentiment analysis from news data to inform trading decisions.

## Features
- **News Sentiment Analysis**: Analyzes recent news using the Alpaca API and makes trading decisions based on sentiment.
- **Automated Trading**: Executes buy/sell orders based on sentiment analysis and risk management.
- **Backtesting**: Tests strategies on historical data using Yahoo Finance.

## Files Overview

### 1. `trading_bot.py`

#### Imports
- **`Alpaca`**: Broker setup for live and paper trading.
- **`YahooDataBacktesting`**: Used for backtesting with historical data.
- **`Strategy`**: Base class for defining trading strategies.
- **`Trader`**: Handles the deployment of the bot.
- **`REST`**: Retrieves dynamic news data via Alpaca.
- **`estimate_sentiment`**: Custom module for sentiment analysis.

#### `MLTrader` Class
- **`initialize(self, symbol="SPY", cash_at_risk=0.5)`**: Sets up the bot with ticker, sleep time, and risk parameters.
- **`position_sizing(self)`**: Determines position size based on available cash and risk.
- **`get_dates(self)`**: Returns today's date and three days ago.
- **`get_news_sentiment(self)`**: Retrieves and analyzes news sentiment for the specified stock.
- **`on_trading_iteration(self)`**: Main trading loop that executes buy/sell decisions based on sentiment.

#### Backtesting & Deployment
- The script sets up and backtests the strategy over a specified period. Deployment code is included but commented out for live trading.

### 2. `sentimenter.py`

#### Sentiment Analysis Setup
- **`tokenizer` and `model`**: Initialized with the FinBERT model for financial sentiment analysis from Hugging Face.
- **`estimate_sentiment(news)`**: Analyzes sentiment from a list of news headlines and returns sentiment and probability.

## Getting Started

### Prerequisites
- **Python 3.8+**
- **Lumibot, Alpaca Account, Hugging Face Transformers, PyTorch**

### Running the Bot
- **Backtesting**: Run the script to test strategies.
- **Live Trading**: Uncomment the relevant section for live trading.

## License
Licensed under the MIT License.

## Acknowledgements
- [Lumibot](https://lumibot.lumiwealth.com)
- [Alpaca](https://alpaca.markets)
- [Hugging Face Transformers](https://huggingface.co/transformers)
