from django.shortcuts import render
from django.urls import reverse
from rest_framework.response import Response
# Create your views here.
from rest_framework.generics import ListAPIView , ListCreateAPIView 
from ..models import *
from ..serializers import *
from .SimulateController import *
from .ComponentController import *
from rest_framework.filters import SearchFilter



class ConfigController(ListCreateAPIView ):
    queryset = DataConfig.objects.all()
    serializer_class = ConfigSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=simulaterID',)
    def get(self, request, *args, **kwargs):
        data = self.list(request,*args, **kwargs).data
        return Response(data = data)
    
    """
            add function take 2 arguments
            data-> list : list of configs dict that needs to add to database
            simulatorData -> integer : simulator ID
     """
    def add(self,data , simulatorData,**kwargs ):
        configList = []
        dataConfig = {}
        for i in data:
            dataConfig = {'frequency':i['frequency'],
                            'noiseLevel':i['noise_level'],
                            'trendCoef':' '.join(str(i) for i in i['trend_coefficients']),
                            'missingPercent':i['missing_percentage'],
                            'outlierPercent':i['outlier_percentage'],
                            'cycle_amplitude':i['cycle_amplitude'],
                            'cycle_frequency':i['cycle_frequency'],
                            'simulaterID':simulatorData,
                            }
            
            # create object of ConfigSerializer
            serielizer = ConfigSerializer(data=dataConfig)
            print(serielizer.is_valid())
            # check if the data are validate or not
            if serielizer.is_valid():
                serielizer.save()

            # DataConfig.save()
            # configs =  self.create(dataConfig , 'custom', **kwargs )
            items = serielizer.data['id']
            componentList = ComponentController().add(i['seasonality_components'] ,items)
            # dataConfig = serielizer.data
            # dataConfig['components'] = componentList
            # configList.append()
        return serielizer.data
    
    def get_simulator_data(self,simulator_id):
        data = DataConfig.objects.all().filter(simulaterID =simulator_id).values()
        data = {
                'data': data,
                }
        return data
    #     pass
    





# import unittest
# class ConfigsTest(unittest.TestCase):
        
#     def getConfigs_success(self):
#         config = ConfigController()
#         dataConfig = [{"frequency":"H1",
#                         "trend_coefficients":"0 2 1 3",
#                         "missing_percentage":0.06,
#                         "outlier_percentage":10,
#                         "noise_level":10,
#                         "cycle_amplitude":0,
#                         "cycle_frequency":1,
#                     }]
#         with self.assertRaises(Exception):
#             file = config.add(dataConfig , 12)


# config =   ConfigsTest()   
# config.getConfigs_success()  





