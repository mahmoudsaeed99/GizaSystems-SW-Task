import pandas as pd
import json
from .ConfigManager.ReaderFactor import ReaderFactor
from .DataProducer.ProducerFactory import ProducerFactory
from .KafkaConsumer import KafkaConsumer
from datetime import datetime
import time
class KafkaToCSV:

    def bridge(self , topicName):

        start_time = time.time()
        kafkaConfig = ReaderFactor().createReader("config.yml", "kafka")
        dataConsumer = KafkaConsumer().comsume(kafkaConfig, topicName)
        end_time = time.time()
        print(end_time - start_time)
        csvProducer = ProducerFactory().createProducer("csv")

        if len(dataConsumer) > 0:
            latest_timestamp = max(dataConsumer, key=lambda x: x['timestamp'])['timestamp']
            timestamp = datetime.strptime(latest_timestamp, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d%H%M%S')
            fileName = "E:/SW/GizaSystems-SW-Task/DjangoProject/myproject/dataSet/kafka_csv_"+str(timestamp)+'.csv'
            df = pd.DataFrame(dataConsumer)
            csvProducer.saveData(df, fileName)
