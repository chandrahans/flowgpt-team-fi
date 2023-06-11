# Responsible for mapping the tickers to an yahoo appropriate format
# Matching logic to deal with inconsistencies in the Yahoo Finance format for currencies

import os 
import pandas as pd

base_currency = "USD" 

ticker_list = [["EUR/USD","EURUSD=X"],
["USD/GBP","GBPUSD=X"],
["pounds","GBPUSD=X"],
["USD/AUD","AUDUSD=X"],
["USD/NZD","NZDUSD=X"],
["EUR/JPY","EURJPY=X"],
["GBP/JPY","GBPJPY=X"],
["EUR/GBP","EURGBP=X"],
["EUR/CAD","EURCAD=X"],
["EUR/SEK","EURSEK=X"],
["EUR/CHF","EURCHF=X"],
["EUR/HUF","EURHUF=X"],
["EUR/JPY","EURJPY=X"],
["USD/CNY","CNY=X"],
["USD/HKD","HKD=X"],
["USD/SGD","SGD=X"],
["USD/INR","INR=X"],
["USD/MXN","MXN=X"],
["USD/PHP","PHP=X"],
["USD/IDR","IDR=X"],
["USD/THB","THB=X"],
["USD/MYR","MYR=X"],
["USD/ZAR","ZAR=X"],
["USD/RUB","RUB=X"],
["USD/JPY","JPY=X"],
["BTCUSD","BTC-USD"],
["ETHUSD","ETH-USD"],
["Tether","USDUSDT-USD"],
["bitcoins","BTC-USD"],
["bitcoin","BTC-USD"],
["BTC","BTC-USD"],
["ethereum","ETH-USD"],
["USD Coin","USDUSDC-USD"],
["ETH","ETH-USD"],
["ETHUSD","ETH-USD"],
["ETH-USD","ETH-USD"],
["SPY US","SPY"]]

ticker_df = pd.DataFrame(ticker_list,columns=['name','yahoo_ticker'])
ticker_df['yahoo_ticker'] = ticker_df['yahoo_ticker'].apply(lambda x:x.strip())

currency_mapping_list = []
for index,row in ticker_df.iterrows():
    if "/" in row['name'] and base_currency in row['name']:
        to_currency = row['name'].split("/")[1]
        currency_mapping_list.append([to_currency,row['yahoo_ticker']])

currency_mapping_df = pd.DataFrame(currency_mapping_list, 
                                  columns=['name','yahoo_ticker'])

ticker_df = pd.concat([ticker_df,currency_mapping_df])

class YahooTickerResolver:

    def __init__(self, ticker):
        self.ticker = ticker.upper()

    def retrieve_yahoo_ticker(self):
        if self.ticker in ticker_df['name'].values:
            return ticker_df[ticker_df['name']==self.ticker]['yahoo_ticker'].values[0]
        print(self.ticker)
        return self.ticker
