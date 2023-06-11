from telegram.ext import MessageHandler, filters, Application, CommandHandler
from rfq_bot.message_connectivity.bot_base import BotBase

WELCOME_MESSAGE = "Hello! Ready to assist with your RFQs"

class TelegramBot(BotBase):
    def __init__(self, config):
        self.application = Application.builder().token(config['TELEGRAM']['api-key']).build()

        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.receive_message))
        self.application.add_handler(CommandHandler("start", self.on_start))
        self.listeners = []

    def start(self):
        self.application.run_polling(1.0)

    async def on_start(self, update, context):
        await self.send_message(update.message.chat_id, WELCOME_MESSAGE)

    async def send_message(self, chat_id, text):
        await self.application.bot.send_message(chat_id, text)

    # Listener should have method async def on_message_received(self, bot: BotBase, message, chat_id):
    def register_listener(self, listener):
        self.listeners.append(listener)

    async def _receive_message(self, update, context):
        chat_id = update.message.chat_id
        text = update.message.text
        print(f"Received message: {text} from chat id: {chat_id}")
        for listener in self.listeners:
            await listener.on_message_received(self, text, chat_id)
