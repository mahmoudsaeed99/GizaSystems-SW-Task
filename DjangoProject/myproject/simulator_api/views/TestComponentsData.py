from django.shortcuts import redirect , render
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from ComponentController import *


from rest_framework.test import APIRequestFactory
# from rest_framework.test import APIClient



# from django.conf import settings
# settings.configure()
class TestComponents():


    def get_component_success (self , data_id):
        data = ComponentController().get_data_component(data_id)
        return data
    
    def add_configs_test(self):
        data = [{
            "frequency":"Weekly",
            "multiplier":1,
            "phase_shift":0,
            "amplitude":3
        }]
        try:
            components = ComponentController().add(data , 4)
        except:
            raise Exception("error")
        return components
    
    
test = TestComponents()
print(test.get_component_success(4))
