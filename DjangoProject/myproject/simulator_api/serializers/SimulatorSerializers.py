
from rest_framework import serializers
from simulator_api.models import *
from rest_framework.response import Response
from ..views.ConfigController import *

from ..views.ConfigManager.SQLDB import *
from .ConfigSerializer import ConfigSerializer

class SimulateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Simulator
        fields = "__all__"

    """
        post function (override) : make this function to get only simulator data from request

    """

    # def create(self, request, **kwargs):
    #     dataset_data = request.data.pop('dataset', [])
    #     try:
    #         if (request.data["producer_type"].lower() == "kafka"):
    #             if ("producer_name" not in request.data.keys() or request.data["producer_name"].lower() == ""):
    #                 raise Exception("you should add kafka topic name")
    #
    #         print(request.data)
    #         serielizer = SimulateSerializer(data=request.data)
    #         self.data = request.data
    #         print(serielizer.is_valid())
    #         if serielizer.is_valid():
    #             self.save()
    #             print(serielizer)
    #             # items = serielizer.data['id']
    #             # configs = ConfigSerializer().create(dataset_data['dataset'], items, **kwargs)
    #         # else:
    #         #     raise Exception("not valid simulator data")
    #     except Exception as e:
    #         print("error in SimulateControl "+str(e))
    #     return Response(serielizer.data)



