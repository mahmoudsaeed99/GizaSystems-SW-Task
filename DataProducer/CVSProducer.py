# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 00:37:11 2023

@author: Mahmoud Saeed
"""


from Producer import Producer


#class CVSProducer inherit from Producer 
#child class

class CVSProducer(Producer):
    
    def saveData(self, data,name):
        data.to_csv(name+".csv")
        return
    
    

