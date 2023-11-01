import pandas as pd
import json
from .ConfigManager.ReaderFactor import ReaderFactor
from .DataProducer.ProducerFactory import ProducerFactory
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from datetime import datetime
class KafkaToCSV:

    def bridge(self , topicName):

        kafkaConsumer = ReaderFactor().createReader(topicName, "kafka")
        csvProducer = ProducerFactory().createProducer("csv")
        dataConsumer = kafkaConsumer.read()
        latest_timestamp = max(dataConsumer, key=lambda x: x['timestamp'])['timestamp']
        timestamp = datetime.strptime(latest_timestamp, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
        fileName = "E:/SW/GizaSystems-SW-Task/DjangoProject/myproject/dataSet/kafka_csv_"+str(timestamp)+'.csv'
        df = pd.DataFrame(dataConsumer)
        csvProducer.saveData(df, fileName)
