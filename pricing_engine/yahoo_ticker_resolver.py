# Responsible for mapping the tickers to an yahoo appropriate format
# Matching logic to deal with inconsistencies in the Yahoo Finance format for currencies

import os 
import pandas as pd

ticker_folder_name = "yahoo_ticker_mapping"
ticker_file_name = "ticker_mapping.txt"
base_currency = "USD" 
path_of_mapping = os.path.join(*[os.getcwd(),
				ticker_folder_name,
				ticker_file_name])

ticker_df = pd.read_csv(path_of_mapping)
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
