# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 22:59:15 2023

@author: Mahmoud Saeed
"""

from fileFactor import fileFactor


class ConfigManager:
    
    def readConfig(self, name ):
        """
       Read config from diff sources.

       Parameters:
           name (String): The file name that contains the configs.
           
       Returns:
           pandas.dataframe: the configs data.
       """
        try:
            file = fileFactor().createFile(name)
        except:
            print("not supported file or no file in this destination")
        configs = file.readConfig()
        return configs
    
    
