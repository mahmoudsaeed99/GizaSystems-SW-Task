# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 23:00:51 2023

@author: Mahmoud Saeed
"""
# from  CSVFile import CSVFile
from ConfigManager.CSVFile import CSVFile
from ConfigManager.XMLFile import XMLFile
from ConfigManager.SQLDB import *

# Class fileFactor help us to return the correct object of file that we want
# to get the data like `csv`.....etc.

class ReaderFactor:
    
    def createReader(self,name ,type_):
        if(type_ == 'csv'):
            return CSVFile(name)
        elif(type_ == 'SQL'):
            return SQLDB(name)
        else:
            raise Exception("not supported file")
        
            
       
        
            
            
            
            