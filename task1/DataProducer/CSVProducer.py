
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 00:37:11 2023

@author: Mahmoud Saeed
"""


from DataProducer.Producer import Producer


#class CVSProducer inherit from Producer 
#child class

class CSVProducer(Producer):
    
    def saveData(self, data,name):
        data.to_csv(name,encoding='utf-8', index=False)
        return
    
    

