from threading import Thread
from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads, dumps
from gestore_personale import GestorePersonale
from mongo import MongoDB
from telegram_bot import TelegramBot
from producer import DispatcherProducer, GitLabProducer
from consumer import DispatcherConsumer, TelegramConsumer, EmailConsumer
from functions import create_kafka_topic, getSMTP
from mongoengine import connect
from terminal import Terminal
from time import sleep
from app import Application
import logging
# Flask
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
# Kafka server
server = "localhost:9092"
# Mongo server
mongo_client = connect('test-db', host='localhost', port=27017)
mongo = MongoDB()
# Email server
email_server = getSMTP()
# Telegram bot
bot_token = "801707462:AAEr53I99kpuBVrOtTaWq_SWLOKiBfu9UoI"
# bot_token = "685399114:AAFbYn40YzI88XQQdganMUOM06u5nO0mxHg"
telegram_bot = TelegramBot(bot_token, mongo)
# Topic name
gitlab_topic_name = "gitlab"
telegram_topic_name = "telegram"
email_topic_name = "email"
topic_name_list = [gitlab_topic_name, telegram_topic_name, email_topic_name]
while not create_kafka_topic(server, topic_name_list):
    continue
print("Kafka topics created successfully")
# Components
dispatcher_producer = DispatcherProducer(KafkaProducer(bootstrap_servers=[server],
                                                       value_serializer=lambda x: dumps(x).encode("utf-8")))
gestore_personale = GestorePersonale(mongo, dispatcher_producer)
dispatcher_consumer = DispatcherConsumer(KafkaConsumer(gitlab_topic_name, bootstrap_servers=[server],
                                                       auto_offset_reset="earliest",
                                                       enable_auto_commit=True,
                                                       auto_commit_interval_ms=300,
                                                       value_deserializer=lambda x: loads(x.decode("utf-8")),
                                                       group_id="my-group"), gestore_personale)
gitlab_producer = GitLabProducer(KafkaProducer(bootstrap_servers=[server],
                                               value_serializer=lambda x: dumps(x).encode("utf-8")))
telegram_consumer = TelegramConsumer(KafkaConsumer(telegram_topic_name,
                                                   bootstrap_servers=[server],
                                                   auto_offset_reset="earliest",
                                                   enable_auto_commit=True,
                                                   auto_commit_interval_ms=300,
                                                   value_deserializer=lambda x: loads(x.decode("utf-8")),
                                                   group_id="my-group"), telegram_bot)
email_consumer = EmailConsumer(KafkaConsumer(email_topic_name,
                                             bootstrap_servers=[server],
                                             auto_offset_reset="earliest",
                                             enable_auto_commit=True,
                                             auto_commit_interval_ms=300,
                                             value_deserializer=lambda x: loads(x.decode("utf-8")),
                                             group_id="my-group"), email_server)
print("Butterfly components created successfully")
# Web view
web_view = Application(mongo)
# Threads
components = dict(start=[telegram_bot, dispatcher_consumer, telegram_consumer, email_consumer, gitlab_producer, web_view],
                  close=[dispatcher_producer, gitlab_producer, dispatcher_consumer, telegram_consumer, email_consumer,
                         telegram_bot, mongo_client, email_server])
threads = [Thread(target=component.start) for component in components["start"]]
list(map(lambda thread: thread.start(), threads))
sleep(1)
terminal_view = Terminal(mongo)
list(map(lambda component: component.close(), components["close"]))
# list(map(lambda thread: thread.join(), threads))
exit()
