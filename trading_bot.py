
#IMPORTS
from lumibot.brokers import Alpaca  #Broker - Explain
from lumibot.backtesting import YahooDataBacktesting  #Backtester - Explain
from lumibot.strategies.strategy import Strategy  #Trading Bot - Explain
from lumibot.traders import Trader  #Deployment capability - Explain
from alpaca_trade_api import REST  #Dynamically gets news data from API
from datetime import datetime
from timedelta import Timedelta
from sentimenter import estimate_sentiment
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

#API key holders - fill with information from Alpaca website
#https://app.alpaca.markets/paper/dashboard/overview
API_KEY = "PK1UT7YPLKSU56A8UZC3"
API_SECRET = "hJr6lEm4hDQlMAYj5EbouiAe4UMlkWto0NdqEmmq"
BASE_URL = "https://paper-api.alpaca.markets/v2"

#Alpaca broker needs a dict passed to it
ALPACA_CREDS = {
    "API_KEY" : API_KEY,
    "API_SECRET" : API_SECRET,
    "PAPER" : True
}

#Creates a class for the strategy
class MLTrader(Strategy) :

    #Runs once when trader is first set up
    def initialize(self, symbol : str = "SPY", cash_at_risk:float = 0.5) :
        self.symbol = symbol  #symbol - ticker symbol representing the stock
        self.sleeptime = "24H"  #Sets whether and when program runs
        self.last_trade = None  #Captures latest trade
        self.cash_at_risk = cash_at_risk  #Sets how much of intial capital we're willing to lose
        self.api = REST(base_url = BASE_URL, key_id = API_KEY, secret_key = API_SECRET)

    def position_sizing(self) :
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)  #Retrieves last price of stock from market
        quantity = round((cash * self.cash_at_risk) / last_price, 0)  #Decides how many to buy
        return cash, last_price, quantity
    
    #Helper function to held get_news() to get the start and end dates
    def get_dates(self) :
        today = self.get_datetime()
        three_days_ago = today - Timedelta(days = 3)
        return today.strftime('%Y-%m-%d'), three_days_ago.strftime('%Y-%m-%d')

    # Uses the Alpaca API to get the news about SPY of last 3 days of date
    def get_news_sentiment(self) :
        today, three_days_ago =  self.get_dates()
        news = self.api.get_news(symbol = self.symbol, 
                              start = three_days_ago, 
                              end = today)  #Gets news between start and end
        news = [ev.__dict__["_raw"]["headline"] for ev in news]  #Reformats the news into readable format (ev = event)
        probability, sentiment = estimate_sentiment(news)
        print(f"\n\n{today} NEWS: {news}\nProbability: {probability}\nSentiment: {sentiment}")
        return probability, sentiment
        

    #Runs everytime there's new data - main investing loop
    def on_trading_iteration(self) :
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_news_sentiment()

        #Only runs if there's enough money to buy at least one
        if cash > last_price:
            if sentiment == "positive" and probability > .999 :
                if self.last_trade == "sell" :
                    self.sell_all()
                order = self.create_order(  #create_order doc: https://lumibot.lumiwealth.com/strategy_methods.orders/strategies.strategy.Strategy.create_order.html
                    self.symbol,
                    quantity,  #quantity to buy, found by self.position_sizing
                    "buy",
                    type = "bracket",
                    take_profit_price = last_price * 1.20,  #Price at which to sell and take profit
                    stop_loss_price = last_price * 0.95  #Price where you sell to minimize loss
                )
                self.submit_order(order)
                self.last_trade = "buy"
            elif sentiment == "negative" and probability > .999 :
                if self.last_trade == "buy" :
                    self.sell_all()
                order = self.create_order(  #create_order doc: https://lumibot.lumiwealth.com/strategy_methods.orders/strategies.strategy.Strategy.create_order.html
                    self.symbol,
                    quantity,  #quantity to sell, found by self.position_sizing
                    "sell",
                    type = "bracket",
                    take_profit_price = last_price * .8,  #Price at which to sell and take profit
                    stop_loss_price = last_price * 1.05  #Price where you sell to minimize loss
                )
                self.submit_order(order)
                self.last_trade = "sell"

#Sets the start and end dates for testing
start_date = datetime(2024, 5, 1)
end_date = datetime(2024, 5, 30)

broker = Alpaca(ALPACA_CREDS)  #EXPLAIN

#Setup of strategy
strategy = MLTrader(name = 'mlstrat', broker = broker,
                    parameters = {"symbol" : "SPY",
                                  "cash_at_risk" : 0.5})

# Backtesting for start and end dates of strategy
strategy.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters = {"symbol" : "SPY",
                  "cash_at_risk" : 0.5}
)

# trader = Trader()
# trader.add_strategy(strategy)
# trader.run_all()