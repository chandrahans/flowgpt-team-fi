import configparser
import sys
from query import Query, QueryHandler

from message_connectivity.telegram_bot import TelegramBot
from message_connectivity.bot_base import BotBase
from rfq_bot.sentiment_analyser.sentiment_engine import SentimentEngine


class EchoReceiver:
    async def on_message_received(self, bot: BotBase, message, chat_id):
        await bot.send_message(chat_id, message)

class QueryRepeater:
    def __init__(self, config) -> None:
        self.query_handler = QueryHandler(config, True)

    async def on_message_received(self, bot: BotBase, message, chat_id):
        formatted_query: Query = self.query_handler.parse(message)
        if formatted_query is not None:
            await bot.send_message(chat_id, str(formatted_query))
        else:
            await bot.send_message(chat_id, "Could not understand that request, please try again!")


def telegram_echo(config):
    telegram_bot: BotBase = TelegramBot(config)
    telegram_bot.register_listener(EchoReceiver())
    telegram_bot.start()


def telegram_query_repeater(config):
    telegram_bot: BotBase = TelegramBot(config)
    telegram_bot.register_listener(QueryRepeater(config))
    telegram_bot.start()


def main() -> None:
    config = configparser.ConfigParser()
    config.read(sys.argv[1])  # read the .ini file path from the first command line argument

    engine = SentimentEngine(config, ['BTCUSD', 'AAPL'])

    telegram_query_repeater(config)


if __name__ == '__main__':
    main()
