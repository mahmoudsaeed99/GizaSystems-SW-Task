from .File import *
import pandas as pd


class XMLFile(File):
    
    def __init__(self,name):
        self.name = name
        
    def readConfig(self):
        pass
    