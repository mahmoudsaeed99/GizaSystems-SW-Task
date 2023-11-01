
from .Producer import Producer
import json
from django.shortcuts import redirect
import requests

class NiFiProducer(Producer):

    def saveData(self, data , urlName):
        try:
            url = "http://localhost:5000/"+str(urlName)
            data['timestamp'] = data['timestamp'].astype(str)
            data['anomaly'] = data['anomaly'].astype(str)
            d = {'value':data['value'][0] , 'timestamp':data['timestamp'][0] , 'anomaly':data['anomaly'][0]}
            r = requests.post(url = url , data = json.dumps(d))
        except Exception as e:
            print("error: data send to nifi unsuccessfully "+str(e))
        # r = redirect()
        return
