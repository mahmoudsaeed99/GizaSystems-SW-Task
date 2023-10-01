# Create your views here.


from .ComponentController import *
from rest_framework.filters import SearchFilter
from simulator_api.serializers.ConfigSerializer import ConfigSerializer
from ..models import *
from django.http import HttpResponse, JsonResponse


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
        """
         add data to Configs model
         `data`(list<dict>): list of data configs dictionary
         `simulatorData`(int): simulator id
        
        """
        configList = []
        dataConfig = {}
        for i in data:
            i['trendCoef'] = ' '.join(str(i) for i in i['trendCoef'])
            i['simulater'] = simulatorData
            # create object of ConfigSerializer
            serielizer = ConfigSerializer(data=i)
            # check if the data are validate or not
            try:
                print(serielizer.is_valid())
                if serielizer.is_valid():
                    serielizer.save()
                    items = serielizer.data['id']
                    componentList = ComponentController().add(i['seasonality_components'] ,items)

            except Exception as e:
                print("error in config control "+str(e))
        return serielizer.data
    
    def get_simulator_data(self,simulator_id):
        """
            return configs for specific simulator
        
        """
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





