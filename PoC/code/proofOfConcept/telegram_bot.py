from telebot import TeleBot
from mongo import MongoDB


class TelegramBot:
    def __init__(self, token: str, mongo: MongoDB):
        self._mongo = mongo
        self._bot = TeleBot(token)

        @self._bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            try:
                self._mongo.update_telegram_id(message.chat.username, message.chat.id)
                self._bot.reply_to(message, "Howdy, how are you doing?")
            except Exception as e:
                self._bot.reply_to(message, str(e))

    def set_bot(self, bot: TeleBot):
        self._bot = bot

        @self._bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            try:
                self._mongo.update_telegram_id(message.chat.username, message.chat.id)
                self._bot.reply_to(message, "Howdy, how are you doing?")
            except Exception as e:
                self._bot.reply_to(message, str(e))

    def get_bot(self):
        return self._bot

    def close(self):
        self._bot.stop_polling()
        self._bot.stop_bot()

    def start(self):
        self._bot.polling()

    def send_message(self, recipient: int, message: str):
        self._bot.send_message(recipient, message)
