from flask import Flask, request, abort
from kafka import KafkaProducer
from abc import abstractmethod


class Producer:
    def __init__(self, producer: KafkaProducer):
        self._producer = producer

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def produce(self, data: dict):
        pass

    def send(self, topic_name: str, data: dict):
        self._producer.send(topic_name, data)

    def close(self):
        self._producer.close()


class DispatcherProducer(Producer):
    def __init__(self, producer: KafkaProducer):
        super().__init__(producer)

    def start(self):
        pass

    def produce(self, data: dict):
        recipients = DispatcherProducer.extract_topic_list(data)
        for topic in recipients.keys():
            data["recipients"] = recipients[topic]
            self.send(topic, data)
            data.pop("recipients")

    @staticmethod
    def extract_topic_list(data: dict):
        return data.pop("recipients")


class GitLabProducer(Producer):
    def __init__(self, producer: KafkaProducer):
        super().__init__(producer)
        self._app = Flask("gitlab_listener")

        @self._app.route('/webhook', methods=['POST'])
        def webhook():
            if request.method == 'POST':
                self.produce(request.json)
                return '', 200
            else:
                abort(400)

    def start(self):
        self._app.run(host="0.0.0.0", port=5000)

    def produce(self, data: dict):
        self.send("gitlab", data)
