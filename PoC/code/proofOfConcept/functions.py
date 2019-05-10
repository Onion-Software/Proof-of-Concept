from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer
from json import loads
from smtplib import SMTP


def create_kafka_topic(server: str, topic_name_list: list):
    topic_list = [NewTopic(name=topic_name, num_partitions=1, replication_factor=1) for topic_name in topic_name_list]
    admin_client = KafkaAdminClient(bootstrap_servers=[server],
                                    client_id='test')
    mock_consumer = KafkaConsumer(
        bootstrap_servers=[server],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        auto_commit_interval_ms=300,
        value_deserializer=lambda x: loads(x.decode("utf-8")),
        group_id="my-group")
    admin_client.delete_topics(mock_consumer.topics())
    mock_consumer.close()
    if len(mock_consumer.topics()) == 0:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        return True
    else:
        return False


def getSMTP():
    email_server = SMTP("smtp.gmail.com", 587)
    email_server.ehlo()
    email_server.starttls()
    email_server.source_address = "softwareonion@gmail.com"
    email_server.login(email_server.source_address, "ipiufiki")
    return email_server


if __name__ == "__main__":
    create_kafka_topic("localhost:9092", ["gitlab", "telegram", "email"])
