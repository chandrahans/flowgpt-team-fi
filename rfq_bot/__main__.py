import configparser
import sys

from message_connectivity.telegram_bot import TelegramBot
from message_connectivity.bot_base import BotBase


class EchoReceiver:
    async def on_message_received(self, bot: BotBase, message, chat_id):
        await bot.send_message(chat_id, message)


def telegram_echo(config):
    telegram_bot: BotBase = TelegramBot(config)
    telegram_bot.register_listener(EchoReceiver())
    telegram_bot.start()


def main() -> None:
    config = configparser.ConfigParser()
    config.read(sys.argv[1])  # read the .ini file path from the first command line argument

    telegram_echo(config)


if __name__ == '__main__':
    main()
