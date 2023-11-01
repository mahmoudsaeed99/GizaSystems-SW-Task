# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 00:30:48 2023

@author: Mahmoud Saeed
"""

from abc import ABC , abstractmethod


# abstract class to save data to any source
#Parent class
class Producer(ABC):
    
    @abstractmethod
    def saveData(self,data,name):
        pass
