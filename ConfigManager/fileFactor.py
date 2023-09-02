# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 23:00:51 2023

@author: Mahmoud Saeed
"""
# from  CSVFile import CSVFile
from ConfigManager.CSVFile import CSVFile
from ConfigManager.XMLFile import XMLFile

# Class fileFactor help us to return the correct object of file that we want
# to get the data like `csv`.....etc.

class fileFactor:
    
    def createFile(self,name):
        """
       Create object file to read the Configs.

       Parameters:
           name(Str): The file name to consider which object will return.
       Returns:
           File(Object): The object of file type .
       """
        if name[-4:] == ".csv":
            return CSVFile(name)
        else:
            raise Exception("file not supported")
            
       
        
            
            
            
            