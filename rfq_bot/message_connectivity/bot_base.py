from abc import ABC, abstractmethod

class BotBase(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    async def send_message(self, chat_id, text):
        pass

    # Listener should have method on_message_received(bot: BotBase, message, chat_id)
    @abstractmethod
    async def register_listener(self, listener):
        pass
