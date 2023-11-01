
from .Producer import Producer
# from kafka import KafkaProducer

import json
import requests
import time
class KafkaProducer(Producer):

    def saveData(self, data , topic_name):
        try:
            from confluent_kafka import Producer
            bootstrap_servers = 'localhost:9092'
            # # Create a Kafka producer instance
            producer_config = {
                "bootstrap.servers": bootstrap_servers
            }
            producer = Producer(producer_config)
            data = {"value":data['value'][0],"timestamp":str(data['timestamp'][0]),
                    "attributeId":str(data['attributeId'][0]) , "assetId":str(data['assetId'][0])}
            serialized_data = json.dumps(data).encode('utf-8')
            producer.produce(topic_name , serialized_data)
            producer.flush()
        except Exception as e:
            print("error: data send to kafka unsuccessfully "+str(e))
        return
