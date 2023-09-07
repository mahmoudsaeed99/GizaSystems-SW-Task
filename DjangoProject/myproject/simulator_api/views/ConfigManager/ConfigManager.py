# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 22:59:15 2023

@author: Mahmoud Saeed
"""

from ReaderFactor import ReaderFactor


class ConfigManager:
    
    def readConfig(self, name , type_ ):
        """
       Read config from diff sources.

       Parameters:
           name (String): The file name that contains the configs.
           
       Returns:
           pandas.dataframe: the configs data.
       """
        try:
            file = ReaderFactor().createReader(name,type_)
        except:
            print("not supported file or no file in this destination")
        file.open()
        return file
    
    
