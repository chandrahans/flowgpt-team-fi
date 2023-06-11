import re
import time
import requests
from bs4 import BeautifulSoup

from rfq_bot.sentiment_analyser.scrappers.scrapper_base import ScrapperBase

from rfq_bot.sentiment_analyser.analysers.sentiment import SentimentAnalyser

# https://github.com/israel-dryer/Yahoo-News-Scraper/blob/master/yahoo-news-scraper.ipynb


class YahooSearch(ScrapperBase):
    def __init__(self, config, sentiment_engine, ticker_list):
        ScrapperBase.__init__(self, config, sentiment_engine)
        self.analyser = SentimentAnalyser(config)
        self.ticker_list = ticker_list

    def _get_article(self, card):
        """Extract article information from the raw html"""
        headline = card.find('h4', 's-title').text
        description = card.find('p', 's-desc').text.strip()

        article = headline + '/n' + description
        return article

    def run(self):
        while True:
            for ticker in self.ticker_list:
                template = 'https://news.search.yahoo.com/search?p={}'
                url = template.format(ticker)

                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')

                cards = soup.find_all('div', 'NewsArticle')

                # extract articles from page
                average_sentiment = 0
                sentiment_count = 0
                for card in cards:
                    article = self._get_article(card)
                    print(article)

                    result = self.analyser.analyse_text(article)
                    print(result)
                    if result is not None:
                        average_sentiment += result
                        sentiment_count += 1

                sentiment = average_sentiment / sentiment_count
                self.sentiment_engine.add_score(ticker, sentiment)

            time.sleep(90)
