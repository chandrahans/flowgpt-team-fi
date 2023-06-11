import time
import requests
from bs4 import BeautifulSoup

from rfq_bot.sentiment_analyser.scrappers.scrapper_base import ScrapperBase

from rfq_bot.sentiment_analyser.analysers.ticker_sentiment import TickerSentimentAnalyser


class Yahoo(ScrapperBase):
    def __init__(self, config, sentiment_engine):
        ScrapperBase.__init__(self, config, sentiment_engine)
        self.analyser = TickerSentimentAnalyser(config)

    def run(self):
        url = 'https://finance.yahoo.com/'

        while True:
            # Send HTTP request to the specified URL and save the response from server in a response object called r
            r = requests.get(url)
            print(r)

            # Create a BeautifulSoup object and specify the parser
            soup = BeautifulSoup(r.text, 'html.parser')

            for news in soup.find_all('div', attrs={'class': 'Cf'}):
                headline = news.find('h3').find('span').text
                print(headline)
                description = news.find('p').text
                print(description)
                result = self.analyser.analyse_text(headline + '/n' + description)
                if result is not None:
                    for item in result:
                        self.sentiment_engine.add_score(item.ticker, item.sentiment)

            time.sleep(90)
