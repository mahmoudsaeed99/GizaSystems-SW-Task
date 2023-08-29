# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 23:00:51 2023

@author: Mahmoud Saeed
"""
from CSVFile import CSVFile


# Class fileFactor help us to return the correct object of file that we want
# to get the data like `csv`.....etc.

class fileFactor:
    
    def createFile(self,name):
        if name[-4:] == ".csv":
            return CSVFile(name)
        else:
            raise Exception("file not supported")
            return
       
        
            
            
            
            