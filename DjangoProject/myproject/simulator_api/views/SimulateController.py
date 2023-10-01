
from .ConfigController import ConfigController
from rest_framework.response import Response
# Create your views here.
from rest_framework.generics import ListCreateAPIView
from ..serializers.SimulatorSerializers import *

from simulator_api.serializers.SimulatorSerializers import *
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from .BuildSimulator import BuildSimulator as BuildSimulator

from .ConfigManager.SQLDB import *

from multiprocessing import Process
import psutil

threads = {}

class SimulateController(ListCreateAPIView ):
    queryset = Simulator.objects.all()
    serializer_class = SimulateSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=id',)

    def post(self, request, *args, **kwargs):
        print("enter")
        """
           receive simulator data and pass each data to the specific model

        """
        # newSimulate = self.create(request.data['startDate'] , *args, **kwargs )

        # Extract all data that related to simulator
        # simulate = {"data":{'startDate':request.data['startDate'],
        #                     'name':request.data['name'],
        #                     'timeSeries_type':request.data['timeSeries_type'],
        #                     'producer_type':request.data['producer_type'],
        #                     }}
        #
        # simkeys = request.data.keys()
        #
        # # Check which attributes that the user add in the request
        # if 'endDate' in simkeys:
        #     simulate['data']['endDate'] = request.data['endDate']
        # else:
        #       simulate['data']['dataSize'] = request.data['dataSize']

        try:
            serielizer = SimulateSerializer(data=request.data)
            # simulate =  self.create(simulate , 'custom', **kwargs )
            if serielizer.is_valid():
                serielizer.save()
                items = serielizer.data['id']
                print(request.data['dataset'])
                configs = ConfigController().add(request.data['dataset'], items, **kwargs)
            else:
                raise Exception("not valid simulator data")
        except Exception as e:
            print("error in SimulateControl "+str(e))
        return Response(serielizer.data)


    def get(self,request, *args, **kwargs):
        """
            return simulator using simulator_id

        """
        simulator_id = request.GET['search']
        config = SQLDB()
        simulatorConfigs = config.read(simulator_id)
        return Response(simulatorConfigs)

    @api_view(['GET'])
    def runSimulator(request):
        """
           Run simulator by recieve the simulator_id to run this simulator

        """
        simulator_id = request.GET.get('simulator_id',-1)
        
        if simulator_id == -1 or simulator_id == "":
            error = {"error":"please input valid id , add key 'simulator_id' and pass valid id value"}
            return Response(error)

        SimulateController().update_status(simulator_id ,"Running")
        config = SQLDB()
        simulatorConfigs = config.read(simulator_id)
        # make exception handling to catch error
        try:

            buildSimulator = BuildSimulator(simulatorConfigs)
            buildSimulator.simulate()
            # process =Process(target= buildSimulator.simulate)
            # process.start()
            # id_ = process.pid
            id_ = 22
            # threads[id_] = buildSimulator
            SimulateController().update_proccess(simulator_id, id_)
            
        except Exception as e:
            SimulateController().update_status(simulator_id ,"Failed")
            return Response({'error':"failed to build simulator "+str(e)})
        
        return Response({'message':"Built simulator: "+str(simulator_id)+" Running in process id : "+str(id_)+""})
        # return simulator

    
    @api_view(['GET'])
    def stopSimulator(request):
        """
          stop simulator using the id of specific simulator
        
        """
        process_id = request.GET.get('process_id',-1)
        if process_id == -1 or process_id == "":
            error = {"error":"please input valid id , add key 'simulator_id' and pass valid id value"}
            return Response(error)
        simulator = Simulator.objects.all().filter(process_id = process_id)[0]
        try:
             psutil.Process(simulator.process_id).terminate()
        except:
            return Response({'message':"Stop building simulator: "+str(simulator.id)+" un-successfully"})

        SimulateController().update_proccess(simulator.id , 0)

        return Response({'message':"Stop building simulator: "+str(simulator.id)+""})

    def update_status(self,simulator_id , newField):
        try:
            simulator = Simulator.objects.get(id = simulator_id)
            simulator.status = newField
            simulator.save()
        except:
            raise Exception("Update Faild")
        
        return
    def update_proccess(self,simulator_id , newField):
        try:
            simulator = Simulator.objects.get(id = simulator_id)
            simulator.process_id = newField
            simulator.save()
        except:
            raise Exception("Update Faild")

        return

    def update_meta(self,simulator_id , newfield):

        """
          update specific simulator 
          `simulator_id`(int): the simulator id the you want to update
          `field`(string) : the field that you want to update
          `newField`(string) : the new data , you want to pass to the field
        
        """
        # simulatorSerializer = SimulateSerializer()
        try:
            simulator = Simulator.objects.get(id = simulator_id)
            simulator.metaData = newfield
            simulator.save()
            # print(simulator.objects.all().values())
        except:
            raise Exception("Update Faild")
        
        return
    
    def get_simulator_status(self,simulator_id):
        """
          return status of specific simulator
        """
        simulator = Simulator.objects.get(pk = simulator_id)
        return simulator.status

    
    
    # override function create
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request['data'])
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return serializer.data
