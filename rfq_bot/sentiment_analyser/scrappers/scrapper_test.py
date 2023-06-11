import time

from rfq_bot.sentiment_analyser.scrappers.scrapper_base import ScrapperBase


class ScrapperTest(ScrapperBase):
    def __init__(self, config, sentiment_engine):
        ScrapperBase.__init__(self, config, sentiment_engine)

    def run(self):
        while True:
            ticker = 'AAPL'
            score = 5 # self.analyser.analyse_text('')
            # Call the add_score method to update the sentiment score
            self.sentiment_engine.add_score(ticker, score)
            # print('score updated')

            time.sleep(1)
