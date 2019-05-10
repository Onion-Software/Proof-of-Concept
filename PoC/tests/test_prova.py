"""

from consumer import EmailConsumer
from kafka import KafkaConsumer
from smtplib import SMTP
import smtpd
import threading
import asyncore
from json import loads, dumps
import pytest


class TestingSMTPServer(smtpd.SMTPServer, threading.Thread):
    def __init__(self, port=25):
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

def test_0():
    smtp_server = TestingSMTPServer()
    smtp_server.start()
    email_server = SMTP("localhost", smtp_server.port)
    email_server.ehlo()
    email_server.starttls()
    email_server.source_address = "softwareonion@gmail.com"
    email_server.login(email_server.source_address, "ipiufiki")
    smtp_server.close()
    self.assertIn(b'hello', smtp_server.received_data)

@pytest.fixture(scope="module")
def email_server():
    email_server = SMTP("smtp.gmail.com", 587)
    email_server.ehlo()
    email_server.starttls()
    email_server.source_address = "softwareonion@gmail.com"
    email_server.login(email_server.source_address, "ipiufiki")
    return email_server


def test_email_sender(email_server):
    data = dict(recipients=["habboclemente@gmail.com"], data="test")
    for recipient in data.pop("recipients"):
        msg = f"From: {email_server.source_address}\nTo: {recipient}\nSubject: Notifica Butterfly\n\n {dumps(data, indent=4)}"
        email_server.sendmail(email_server.source_address, recipient, msg)
ì    assert True


def test_email_consumer():
    email_consumer = EmailConsumer(KafkaConsumer(bootstrap_servers=["localhost:9092"],
                                                 auto_offset_reset="earliest",
                                                 enable_auto_commit=True,
                                                 auto_commit_interval_ms=300,
                                                 value_deserializer=lambda x: loads(x.decode("utf-8")),
                                                 group_id="my-group"), "softwareonion@gmail.com", "ipiufiki")
    data = dict(recipients=["habboclemente@gmail.com"], data="test")
    email_consumer.consume(data)
    assert True
"""