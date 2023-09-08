from .DB import *
import pandas as pd


class SQLDB(DB):
    userName = ''
    password = ''
    dbName = ''
    def __init__(self, tableName):
        super().__init__(tableName)

    def open(self):
        pass

    def read(self):
        pass

    
