import configparser
import random
import sys
from rfq_bot.query import Query, QueryHandler

from pricing_engine.pricing_engine import PricingEngine
from rfq_bot.message_connectivity.telegram_bot import TelegramBot
from rfq_bot.message_connectivity.bot_base import BotBase
from rfq_bot.sentiment_analyser.sentiment_engine import SentimentEngine

ERROR_MSG = "Could not understand that request, please try again!\n\
Try for example: '2w 500 BTC', 'I wanna buy 10 ETH', 'Can I have an offer on 10 BTC and 20 ETH' etc."

def get_random_message():
    return random.choice(["Hold on! I'm pricing it, ", 
                   "Give me a sec, ", 
                   "Getting you the best prices, "
                   "One sec, "])

class QueryRepeater:
    def __init__(self, config) -> None:
        self.verbose = True if config['COMMON']['verbose'] == "True" else False
        self.query_handler = QueryHandler(config)

    async def on_message_received(self, bot: BotBase, message, chat_id, first_name):
        await bot.send_message(chat_id, get_random_message() + f" {first_name}!")
        formatted_query: list = self.query_handler.parse(message)
        if not formatted_query:
            await bot.send_message(chat_id, ERROR_MSG)
        for listing_query in formatted_query:
            if formatted_query is not None:
                await bot.send_message(chat_id, str(PricingEngine(listing_query)))
            else:
                await bot.send_message(chat_id, ERROR_MSG)


def main() -> None:
    config = configparser.ConfigParser()
    # read the .ini file path from the first command line argument
    config.read(sys.argv[1])

    engine = SentimentEngine(config, ['BTCUSD', 'AAPL'])
    telegram_bot: BotBase = TelegramBot(config)
    telegram_bot.register_listener(QueryRepeater(config))

    for _ in range(5):
        try:
            print("Starting the RFQ bot server...")
            telegram_bot.start()
        except Exception as e:
            print(
                f"An exception ({e}) occured during runtime, restarting the bot server...")
            engine.stop()
            telegram_bot.application.stop()


if __name__ == '__main__':
    main()
