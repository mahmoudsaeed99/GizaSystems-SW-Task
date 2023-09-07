from django.shortcuts import render
from .ConfigController import ConfigController
from rest_framework.response import Response
# Create your views here.
from rest_framework.generics import ListAPIView , ListCreateAPIView 
from ..models import *
from ..serializers import *
from rest_framework import status
import datetime
from django.shortcuts import redirect
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter

class SimulateController(ListCreateAPIView ):
    queryset = Simulator.objects.all()
    serializer_class = SimulateSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=id',)
    def get(self, request, *args, **kwargs):
        data = self.list(request,*args, **kwargs).data
        return Response(data = data)
    
    """
        post function (override) : make this function to get only simulator data from request

    """
    def post(self, request, *args, **kwargs):
        # newSimulate = self.create(request.data['startDate'] , *args, **kwargs )

        # Extract all data that related to simulator
        simulate = {'data':{'startDate':request.data['startDate'],
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
        
        simulate =  self.create(simulate , 'custom', **kwargs )
        items = simulate.data['id']
        configs = ConfigController().add(request.data['dataset'], items, **kwargs)
        return Response(simulate.data)
    
    def update_status(self,simulator_id , newStatus):
        # simulatorSerializer = SimulateSerializer()
        try:
            simulator = Simulator.objects.get(pk = simulator_id)
            simulator.status = newStatus
            simulator.save()
        except:
            raise Exception("Update Faild")
        
        return
    
    def get_simulator_status(self,simulator_id):
        simulator = Simulator.objects.get(pk = simulator_id)
        return simulator.status

    
    
    # override function create
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request['data'])
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return serializer.data










