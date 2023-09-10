# settings.configure()

from django.shortcuts import redirect , render
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from SimulateController import SimulateController


from rest_framework.test import APIRequestFactory
# from rest_framework.test import APIClient



# from django.conf import settings
# settings.configure()
class TestSimulator():
    def __init__(self, id):
        self.id = id

    def get_simulator_success (self ):
        s = SimulateController().get_simulator(self.id)
        return s
    
    def simulator_status_success(self):
        simulator = SimulateController().get_simulator_status(self.id)
        return simulator
    
    def runSimulator():
        factor = APIRequestFactory()
        r = factor.get("http://127.0.0.1:8000/simulate/run/",{'simulator_id':94})
        return r

test = TestSimulator(94)
print(test.get_simulator_success())





