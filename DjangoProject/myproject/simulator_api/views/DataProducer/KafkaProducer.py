
from .Producer import Producer
# from kafka import KafkaProducer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
import json
import requests
import time
class KafkaProducer(Producer):
    def __init__(self):
        from confluent_kafka import Producer
        bootstrap_servers = 'localhost:9092'
        # # Create a Kafka producer instance
        producer_config = {
                "bootstrap.servers": bootstrap_servers,
                'acks': 0,
        }
        self.admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})
        self.producer = Producer(producer_config)
    def saveData(self, data , topic_name):
        try:
            data = {"value":data['value'][0],"timestamp":str(data['timestamp'][0]),
                    "attributeId":str(data['attributeId'][0]) , "assetId":str(data['assetId'][0])}
            start_time = time.time()
            serialized_data = json.dumps(data).encode('utf-8')
            self.create_topic(topic_name)
            self.producer.produce(topic_name , serialized_data)
            self.producer.flush()
            end_time = time.time()
            print(end_time - start_time)
        except Exception as e:
            print("error: data send to kafka unsuccessfully "+str(e))
        return
    def create_topic(self , topic_name):
        try:
            topic_metadata = self.admin_client.list_topics(timeout=5)
            if topic_name not in topic_metadata.topics:
                # The topic does not exist, create it
                new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
                self.admin_client.create_topics([new_topic])
        except KafkaException as e:
            print(f"Error while creating topic: {e}")
