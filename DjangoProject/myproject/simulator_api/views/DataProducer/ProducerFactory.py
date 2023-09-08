from .CSVProducer import *
from .JsonProducer import *
from .XMLProducer import *

class ProducerFactory():
    
    def createProducer(self , name , type_):
        if type_.lower() == 'csv':
            return CSVProducer()
        elif type_.lower() == 'xml':
            return XMLProducer()    
        
        