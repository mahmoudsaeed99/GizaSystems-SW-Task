
from rest_framework import serializers
from simulator_api.models import *
from rest_framework.response import Response
from ..views.ConfigController import *

from ..views.ConfigManager.SQLDB import *


class SimulateSerializer(serializers.ModelSerializer):

    # dataConfig = serializers.StringRelatedField(many=True)
    class Meta:
        model = Simulator
        fields = "__all__"

    """
        post function (override) : make this function to get only simulator data from request

    """
    def post(self, request, *args, **kwargs):
        print("enter")
        """
           receive simulator data and pass each data to the specific model

        """
        # newSimulate = self.create(request.data['startDate'] , *args, **kwargs )

        # Extract all data that related to simulator
        simulate = {"data":{'startDate':request.data['startDate'],
                            'name':request.data['name'],
                            'timeSeries_type':request.data['timeSeries_type'],
                            'producer_type':request.data['producer_type'],
                            }}

        simkeys = request.data.keys()

        # Check which attributes that the user add in the request
        if 'endDate' in simkeys:
            simulate['data']['endDate'] = request.data['endDate']
        else:
              simulate['data']['dataSize'] = request.data['dataSize']

        print("enter")
        simulate =  self.create(simulate , 'custom', **kwargs )
        items = simulate.data['id']
        configs = ConfigController().add(request.data['dataset'], items, **kwargs)
        return Response(simulate.data)


    def get_simulator(self,simulator_id):
        """
            return simulator using simulator_id

        """
        config = SQLDB()
        simulatorConfigs = config.read(simulator_id)
        return simulatorConfigs


        


