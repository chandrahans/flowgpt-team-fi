import threading

from rfq_bot.sentiment_analyser.scrappers.scrapper_test import ScrapperTest
from rfq_bot.sentiment_analyser.scrappers.yahoo import Yahoo
from rfq_bot.sentiment_analyser.scrappers.yahoo_search import YahooSearch


DEFAULT_SENTIMENT = 5

class SentimentEngine:
    def __init__(self, config, ticker_list, verbose=False):
        self.verbose = verbose
        self.score_lock = threading.Lock()
        self.ticker_scores = {ticker: DEFAULT_SENTIMENT for ticker in ticker_list}

        self.scrappers = [
            # Yahoo(config, self),
            YahooSearch(config, self, ticker_list, self.verbose),
            # ScrapperTest(config, self),
        ]

        for scrapper in self.scrappers:
            scrapper.start()

    def add_score(self, ticker, score):
        with self.score_lock:
            # make better algo not just update previous score
            self.verbose and print(f'Changing {ticker} score to {score}')
            self.ticker_scores[ticker] = score

    def get_ticker_score(self, ticker):
        with self.score_lock:
            return self.ticker_scores[ticker]
