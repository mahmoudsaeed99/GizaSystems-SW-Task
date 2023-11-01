from .CSVProducer import *
from .JsonProducer import *
from .KafkaProducer import KafkaProducer
from .XMLProducer import *
from .NiFiProducer import *

class ProducerFactory():
    
    def createProducer(self, type_):
        if type_.lower() == 'csv':
            return CSVProducer()
        elif type_.lower() == 'xml':
            return XMLProducer()    
        elif type_.lower() == "nifi":
            return NiFiProducer()
        elif type_.lower() == "kafka":
            return KafkaProducer()
