
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from ..serializers import *
from ..models import *
from django.http import JsonResponse
from .ConfigController import ConfigController
from .ComponentController import *

from sklearn.preprocessing import MinMaxScaler


from datetime import datetime, timedelta
from .TimeGeneration import TimeSeriesGeneration
# from .ConfigManager.ConfigManager import *
from .ConfigManager.ConfigManager import *
# import Components.AdditionalComponent
from .Components.CyclesComponent import *
from .Components.MissingValuesComponent import *
from .Components.NoiseComponent import *
from .Components.OutliersComponent import *
from .Components.SeasonalComponent import *
from .Components.TrendComponent import *
from .DataProducer.ProducerFactory import *
import threading 

import time




class BuildSimulator(threading.Thread):
   
    def __init__(self,simulator_id,simulator):
         self.simulator_id = simulator_id
         self.simulator = simulator
         threading.Thread.__init__(self)   


    def run(self):
        from .SimulateController import SimulateController
        meta_data = []
        counter = 0
        
        data = ConfigController().get_simulator_data(self.simulator_id)
        while( SimulateController().get_simulator_status(self.simulator_id)== 'Running'):
            # time_series_generate = TimeSeriesGeneration(simulator['start_date'] ,
            #                                              simulator['start_date'] + timedelta(days=simulator['dataSize']))  
            
            if SimulateController().get_simulator_status(self.simulator_id) != 'Running':
                raise Exception("stopped")

            for i in data['data']:
                # date_rng = time_series_generate.generate(i['frequency'])
                components = ComponentController().get_data_component(i['id'])
                
                for j in components['components']:
                    # chekc threading with sleep() function
                    time.sleep(20)
                    # seasonal_component = SeasonalComponent().add_daily(date_rng,
                    #                                                 j['frequency'],
                    #                                                 season_type=simulator['timeSeries_type'])  
                     
                    # trend = [int(i) for i in i['trendCoef'].split()]  
                    # trend_component = TrendComponent().addComponent(date_rng, trend, data_size=simulator['dataSize'],
                    #                 data_type=simulator['timeSeries_type'])
                    
                    # cyclic_component = CyclesComponent().addComponent(date_rng, i['cycle_frequency'],
                    #                                                    season_type=simulator['dataSize'])
                    
                    # if simulator['dataSize'] == 'multiplicative':
                    #     data = seasonal_component *  trend_component * cyclic_component
                    # else:
                    #     data = seasonal_component + trend_component + cyclic_component
                    
                    # # Create a MinMaxScaler instance
                    # scaler = MinMaxScaler(feature_range=(-1, 1))
                    # data = scaler.fit_transform(data.values.reshape(-1, 1))
                    
                    # data = NoiseComponent.addComponent(data, i['noiseLevel'])  
                    
                    # data, anomaly = OutliersComponent.addComponent(data, i['outlierPercent'])

                    # data = MissingValuesComponent.addComponent(data, i['missingPercent'])

                    # df = pd.DataFrame({'value': data, 'timestamp': date_rng, 'anomaly': anomaly})
                    # # df.to_csv('sample_datasets/' + str(counter) + '.csv', encoding='utf-8', index=False)
                    # counter +=1
                    # fileName = i['id']+"_"+j['id'] + '.csv'
                    # producer = ProducerFactory().createProducer(fileName , 'csv')
                    # producer.saveData(df,fileName)
                    # meta_data.append({'simulator':simulator['id'],
                    #                   'dataConfig':i['id'],
                    #                   'components':j['id'],
                    #                  'fileName': fileName,})
                    
                    
            # meta_data_df = pd.DataFrame.from_records(meta_data)
            # print(simulator['startDate'])
            meta_data_name = 'sample_datasets/meta_data+'+self.simulator_id+'.csv'
            # producer.saveData(meta_data_df , meta_data_name)
            print("enter22")
            SimulateController().update_field(self.simulator_id ,"metaData" ,meta_data_name )  
            SimulateController().update_field(self.simulator_id ,"status" , "Success")      
            return  Response({'message':"Stop building simulator: "+self.simulator_id+" successfully"})
        
