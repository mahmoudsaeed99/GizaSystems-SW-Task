# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 22:59:15 2023

@author: Mahmoud Saeed
"""

from fileFactor import fileFactor


class ConfigManager:
    
    def readConfig(self, name ):
        file = fileFactor().createFile(name)
        configs = file.readConfig()
        return configs
    
    