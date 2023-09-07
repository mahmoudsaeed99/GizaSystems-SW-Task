from DataProducer.CSVProducer import *
from DataProducer.JsonProducer import *
from DataProducer.XMLProducer import *

class ProducerFactory():
    
    def createProducer(self , name , type_):
        if type_.lower() == 'csv':
            return CSVProducer()
        elif type_.lower() == 'xml':
            return XMLProducer()    
        
        