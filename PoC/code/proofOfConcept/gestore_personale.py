from mongo import MongoDB
from producer import Producer


class GestorePersonale:
    def __init__(self, mongo: MongoDB, producer: Producer):
        self._producer = producer
        self._mongo = mongo

    def notify(self, data: dict):
        recipients = self._mongo.get_interested_recipients(data["project"]["web_url"])
        if recipients:
            self.add_preferences(data, recipients)

    def add_preferences(self, data: dict, recipients: dict):
        data["recipients"] = recipients
        self._producer.produce(data)
