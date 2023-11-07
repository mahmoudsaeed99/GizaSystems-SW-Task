
from confluent_kafka import Consumer , KafkaError
import json
from django.conf import settings
import pandas as pd
import time

class KafkaMessageDeserializer:
    """ Kafka Deserializer class """
    def __init__(self, schema):
        self.schema = schema

    def deserialize(self, message):
        try:
            message = json.loads(message.decode('utf-8'))
            # Check if the message adheres to the schema
            if all(key in message for key in self.schema.keys()):
                return message
            else:
                # Handle schema validation error, e.g., log the error
                return None
        except json.JSONDecodeError:
            # Handle deserialization error, e.g., log the error
            return None


class KafkaConsumer():

    def comsume(self , config , topic_name):
        schema = {"value": "value1","timestamp":"timestamp1",
                    "attributeId":"attributeId1" , "assetId":"assetId1"}
        # Define the Kafka broker(s)
        bootstrap_servers = config.read("kafka.broker_url")
        # Define the topic(s) to consume from
        topic = topic_name
        conf = {'bootstrap.servers': bootstrap_servers,
        'group.id': settings.KAFKA_GROUP_ID,
                'auto.offset.reset': 'latest'}
        # Create a Kafka consumer instance
        consumer = Consumer(conf)
        consumer.subscribe([topic])
        values = []
        last_message_time = time.time()

        message_deserializer = KafkaMessageDeserializer(schema)
        while True:
            start_time = time.time()
            msg = consumer.poll(1.0)

            if msg is None:
                if time.time() - last_message_time > 50:  # Adjust the timeout as needed (60 seconds in this example)
                    print("No data received for too long. Stopping the consumer.")
                    consumer.close()
                    break
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print("Error: %s" % msg.error())
            else:
                message = msg.value()
                deserialized_message = message_deserializer.deserialize(message)
                if deserialized_message is not None:
                    values.append(deserialized_message)
                    last_message_time = time.time()
        consumer.close()
        return values

