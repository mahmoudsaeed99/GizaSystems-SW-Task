# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 00:16:49 2023

@author: Mahmoud Saeed
"""

from abc import ABC , abstractmethod
from ConfigManager.Reader import *
class File(Reader,ABC):
    def __init__(self , fileName):
        self.fileName = fileName
    
    
