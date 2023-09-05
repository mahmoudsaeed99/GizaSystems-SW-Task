
from ConfigManager.Reader import *
from abc import ABC , abstractmethod

class DB(Reader,ABC):
    def __init__(self , tableName):
        self.tableName = tableName

