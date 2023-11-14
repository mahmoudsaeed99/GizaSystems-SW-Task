from .ConfigController import ConfigController
from rest_framework.response import Response
# Create your views here.
from rest_framework.generics import ListCreateAPIView
from ..serializers.SimulatorSerializers import *

from simulator_api.serializers.SimulatorSerializers import *
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from .BuildSimulator import BuildSimulator as BuildSimulator
from .ConfigManager.ReaderFactor import ReaderFactor
from .DataProducer.ProducerFactory import ProducerFactory
from .ConfigManager.SQLDB import *
from .KafkaToCSV import KafkaToCSV
from multiprocessing import Process
import psutil
import threading

threads = {}

class SimulateController(ListCreateAPIView ):
    queryset = Simulator.objects.all()
    serializer_class = SimulateSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=id',)

    def post(self, request, *args, **kwargs):
        """
           receive simulator data and pass each data to the specific model

        """
        # return(SimulateSerializer().create(request))
        try:
            if (request.data["producer_type"].lower() == "kafka"):
                if ("producer_name" not in request.data.keys() or request.data["producer_name"].lower() == ""):
                    raise Exception("you should add kafka topic name")

            dataset_data = request.data.pop('dataset', [])
            serielizer = SimulateSerializer(data=request.data)
            print("request.data:", request.data)
            print("dataset_data:", dataset_data)
            # simulate =  self.create(simulate , 'custom', **kwargs )
            print(serielizer.is_valid())
            if serielizer.is_valid():
                serielizer.save()
                items = serielizer.data['id']
                print(1)
                configs = ConfigController().add(dataset_data, items, **kwargs)
            # else:
            #     raise Exception("not valid simulator data")
        except Exception as e:
            print("error in SimulateControl "+str(e))
        return Response(request.data)


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
        #kafka to csv
        kafkaToCsv = KafkaToCSV()
        kafka_consumer = threading.Thread(target=kafkaToCsv.bridge , args=[simulatorConfigs['producer_name']])
        kafka_consumer.daemon = True  # This allows the thread to exit when the main application exits.
        kafka_consumer.start()
        #------------
        # make exception handling to catch error
        try:

            buildSimulator = BuildSimulator(simulatorConfigs)
            buildSimulator.simulate()
            # process =Process(target= buildSimulator.simulate)
            # process.start()
            id_ = 1555
            # id_ = process.pid
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
