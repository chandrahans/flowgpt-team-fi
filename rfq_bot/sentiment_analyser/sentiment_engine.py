import threading

from rfq_bot.sentiment_analyser.scrappers.scrapper_test import ScrapperTest
from rfq_bot.sentiment_analyser.scrappers.yahoo import Yahoo


class SentimentEngine:
    def __init__(self, config):
        self.score_lock = threading.Lock()
        self.ticker_scores = {}

        self.scrappers = [
            Yahoo(config, self),
            # ScrapperTest(config, self),
        ]

        for scrapper in self.scrappers:
            scrapper.start()

    def add_score(self, ticker, score):
        with self.score_lock:
            # make better algo not just update previous score
            print(f'Changing {ticker} score to {score}')
            self.ticker_scores[ticker] = score

    def get_ticker_score(self, ticker):
        with self.score_lock:
            return self.ticker_scores[ticker]

    def set_ticker_list(self, ticker_list):
        self.ticker_scores = {ticker: 5 for ticker in ticker_list}
