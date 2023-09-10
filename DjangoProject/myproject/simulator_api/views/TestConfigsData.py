# settings.configure()

from django.shortcuts import redirect , render
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from ConfigController import *


from rest_framework.test import APIRequestFactory
# from rest_framework.test import APIClient



# from django.conf import settings
# settings.configure()
class TestConfigs():


    def get_simulator_success (self , simulator_id):
        data = ConfigController().get_simulator_data(simulator_id)
        return data
    
    def add_configs_test(self):
        data =[{
        "frequency":"H1",
        "trend_coefficients":[0,2,1,3],
        "missing_percentage":0.06,
        "outlier_percentage":10,
        "noise_level":10,
        "cycle_amplitude":0,
        "cycle_frequency":1,
        "seasonality_components":[{
            "frequency":"Weekly",
            "multiplier":1,
            "phase_shift":0,
            "amplitude":3
        }]
        }]
        try:
            simulator = ConfigController().add(data , 12)
        except:
            raise Exception("error")
        return simulator
    

test = TestConfigs()
print(test.get_simulator_success(94))





