




from File import File
import pandas as pd


class CSVFile(File):
    
    def __init__(self,name):
        self.name = name;
        
    def readConfig(self):
        configs = pd.read_csv(self.name)
        return configs
    
    




