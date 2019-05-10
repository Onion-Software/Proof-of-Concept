from consumer import EmailConsumer
from kafka import KafkaConsumer
from smtplib import SMTP
import smtpd
import threading
import asyncore
from json import loads, dumps
import pytest


class TestingSMTPServer(smtpd.SMTPServer, threading.Thread):
    def __init__(self, port=5004):
        smtpd.SMTPServer.__init__(
            self,
            ('localhost', port),
            ('localhost', port),
            decode_data=False
        )
        self.port = port
        threading.Thread.__init__(self)

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        self.received_peer = peer
        self.received_mailfrom = mailfrom
        self.received_rcpttos = rcpttos
        self.received_data = data

    def run(self):
        asyncore.loop()


@pytest.fixture(scope="module")
def smtp_server():
    return TestingSMTPServer()


@pytest.fixture(scope="module")
def email_server(smtp_server):
    email_server = SMTP("localhost", smtp_server.port)
    email_server.source_address =  "sender@lolloneoneone.com"
    return email_server

@pytest.fixture(scope="module")
def email_consumer(email_server):
    return EmailConsumer(KafkaConsumer("test",
                                       bootstrap_servers=["localhost:9092"],
                                       auto_offset_reset="earliest",
                                       enable_auto_commit=True,
                                       auto_commit_interval_ms=300,
                                       value_deserializer=lambda x: loads(x.decode("utf-8")),
                                       group_id="my-group"), email_server)


def test_0(smtp_server):
    smtp_server.start()
    email_server = SMTP("localhost", smtp_server.port)
    data = dict(recipients=["testlolloneoneone.com"], data="hello")
    for recipient in data.pop("recipients"):
        msg = f"From: {email_server.source_address}\nTo: {recipient}\n" \
            f"Subject: Notifica Butterfly\n\n {dumps(data, indent=4)}"
        email_server.sendmail("sender@lolloneoneone.com", recipient, msg)
        email_server.close()
        smtp_server.close()
        assert "sender@lolloneoneone.com" in smtp_server.received_mailfrom
        assert b"hello" in smtp_server.received_data


def test_email_consumer(smtp_server, email_server, email_consumer):
    smtp_server.start()
    data = dict(recipients=["testlolloneoneone.com"], data="hello")
    email_consumer.consume(data)
    email_server.close()
    smtp_server.close()
    assert "sender@lolloneoneone.com" in smtp_server.received_mailfrom
    assert b"hello" in smtp_server.received_data