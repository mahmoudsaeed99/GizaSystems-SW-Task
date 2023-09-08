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
from .BuildSimulator import BuildSimulator as BuildSimulator


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
    

    def get_simulator(self,simulator_id):
        data = Simulator.objects.all().filter(id =simulator_id).values()
        data = {
                'simulator': data,
                }
        return data
    

    @api_view(['GET'])
    def runSimulator(request):
        simulator_id = request.GET.get('simulator_id',-1)
        
        if simulator_id == -1 or simulator_id == "":
            error = {"error":"please input valid id , add key 'simulator_id' and pass valid id value"}
            return Response(error)
        # self.as_view
        # request = redirect('http://127.0.0.1:8000/simulate/?search='+simulator_id+'')
        SimulateController().update_field(simulator_id ,"status" ,"Running")
        # simulator = redirect('http://127.0.0.1:8000/simulate/?search='+simulator_id+'')
        simulator = SimulateController().get_simulator(simulator_id)
        # return Response(simulator['simulator'][0]['id'])
        # dataConfigs = redirect('http://127.0.0.1:8000/simulate/configs/?search='+simulator_id+'')
        # return dataConfigs
        try:
            BuildSimulator().buildSimulator(simulator_id,simulator['simulator'][0])
        
        except:
            SimulateController().update_field(simulator_id ,"status" , "Failed")
            return Response({'error':"failed to build simulator"})
        
        
        
        return Response({'message':"Built simulator: "+simulator_id+" successfully"})
        # return simulator

    
    @api_view(['GET'])
    def stopSimulator(request):
        simulator_id = request.GET.get('simulator_id',-1)
        
        if simulator_id == -1 or simulator_id == "":
            error = {"error":"please input valid id , add key 'simulator_id' and pass valid id value"}
            return Response(error)
        SimulateController().update_field(simulator_id, "status" , "Failed")
        
        return Response({'message':"Stop building simulator: "+simulator_id+" successfully"})
        pass

    def update_field(self,simulator_id , field , newfield):
        # simulatorSerializer = SimulateSerializer()
        try:
            simulator = Simulator.objects.get(pk = simulator_id)
            if field == 'status':
                simulator.status = newfield
            elif field == 'metaData':
                simulator.metaData = newfield
            simulator.save()
            # print(simulator.objects.all().values())
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










