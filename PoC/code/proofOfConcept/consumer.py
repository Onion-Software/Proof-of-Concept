from kafka import KafkaConsumer
from abc import abstractmethod
from gestore_personale import GestorePersonale
from telegram_bot import TelegramBot
from smtplib import SMTP
from json import dumps


class Consumer:
    def __init__(self, consumer: KafkaConsumer):
        self._consumer = consumer

    def start(self):
        for message in self._consumer:
            self.consume(message.value)

    def get_topic_list(self):
        return self._consumer.topics()

    def get_subscription(self):
        return self._consumer.subscription()

    def close(self):
        self._consumer.close()

    @abstractmethod
    def consume(self, data: dict):
        pass


class DispatcherConsumer(Consumer):
    def __init__(self, consumer: KafkaConsumer, gestore: GestorePersonale):
        super().__init__(consumer)
        self._gestore = gestore

    def consume(self, data: dict):
        self._gestore.notify(data)


class TelegramConsumer(Consumer):
    def __init__(self, consumer: KafkaConsumer, bot: TelegramBot):
        super().__init__(consumer)
        self._bot = bot

    def consume(self, data: dict):
        for recipient in self.extract_recipient_list(data):
            self._bot.send_message(recipient, str(data))

    @staticmethod
    def extract_recipient_list(data: dict):
        return data.pop("recipients")


class EmailConsumer(Consumer):
    def __init__(self, consumer: KafkaConsumer, server: SMTP):
        super().__init__(consumer)
        self._server = server
        print(str(self._server.source_address))

    def consume(self, data: dict):
        for recipient in self.extract_recipient_list(data):
            msg = f"From: {self._server.source_address}\nTo: {recipient}\nSubject: Notifica Butterfly\n\n{dumps(data, indent=4)}"
            self._server.sendmail(self._server.source_address, recipient, msg)

    @staticmethod
    def extract_recipient_list(data: dict):
        return data.pop("recipients")
