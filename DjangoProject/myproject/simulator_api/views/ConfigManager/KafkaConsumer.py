
from .File import File
from confluent_kafka import Consumer , KafkaError
import json
from django.conf import settings
import pandas as pd
import time
class KafkaConsumer(File):

    def open(self):

        pass
    def read(self):
        # Define the Kafka broker(s)
        bootstrap_servers = 'localhost:9092'
        # Define the topic(s) to consume from
        topic = self.fileName
        conf = {'bootstrap.servers': bootstrap_servers,
        'group.id': settings.KAFKA_GROUP_ID,
                'auto.offset.reset': 'latest'}
        # Create a Kafka consumer instance
        consumer = Consumer(conf)
        consumer.subscribe([topic])
        values = []
        last_message_time = time.time()
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                if time.time() - last_message_time > 10:  # Adjust the timeout as needed (60 seconds in this example)
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
                message = json.loads(message.decode('utf-8'))
                values.append(message)
        consumer.close()
        return values

