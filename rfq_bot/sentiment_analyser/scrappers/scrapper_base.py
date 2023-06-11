import threading

from rfq_bot.sentiment_analyser.analysers.ticker_sentiment import TickerSentimentAnalyser

from abc import ABC


class ScrapperBase(ABC, threading.Thread):
    def __init__(self, config, sentiment_engine):
        threading.Thread.__init__(self)
        self.sentiment_engine = sentiment_engine
        self.analyser = TickerSentimentAnalyser(config)
