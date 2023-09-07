
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from ..serializers import *
from ..models import *
from django.http import JsonResponse
from .SimulateController import *
from .ConfigController import ConfigController
from .ComponentController import *


class RunSimulator():

    @api_view(['GET'])
    def runSimulator(request):
        simulator_id = request.GET.get('simulator_id',-1)
        
        if simulator_id == -1 or simulator_id == "":
            error = {"error":"please input valid id , add key 'simulator_id' and pass valid id value"}
            return Response(error)
        # self.as_view
        # request = redirect('http://127.0.0.1:8000/simulate/?search='+simulator_id+'')
        SimulateController().update_status(simulator_id , "Running")
        simulator = redirect('http://127.0.0.1:8000/simulate/?search='+simulator_id+'')
        # dataConfigs = redirect('http://127.0.0.1:8000/simulate/configs/?search='+simulator_id+'')
        # return dataConfigs
        try:
            RunSimulator().buildSimulator(simulator_id,simulator)
        
        except:
            SimulateController().update_status(simulator_id , "Failed")
            return Response({'error':"failed to build simulator"})
        
        SimulateController().update_status(simulator_id , "Success")
        return Response({'message':"build simulator: "+simulator_id+" successfully"})
        # return simulator
    

    def buildSimulator(self,simulator_id,simulator):
        data = ConfigController().get_simulator_data(simulator_id)
        while( SimulateController().get_simulator_statuss(simulator_id)== 'Running'):
            for i in data['data']:
                components = ComponentController().get_data_component(i['id'])
                for j in data['components']:
                    pass
                
                # return Response(components)
        pass
