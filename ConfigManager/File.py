# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 00:16:49 2023

@author: Mahmoud Saeed
"""

from abc import ABC , abstractmethod

class File(ABC):
    
    @abstractmethod
    def readConfig(self):
        pass
    
    