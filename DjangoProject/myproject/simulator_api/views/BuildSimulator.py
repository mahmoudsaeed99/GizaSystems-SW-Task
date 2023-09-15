
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
   
    def __init__(self,simulatorConfigs):
         self.simulatorConfigs = simulatorConfigs
         threading.Thread.__init__(self)   

    def stop(self):
        self._stop.set()
    def run(self):
        from .SimulateController import SimulateController
        meta_data = []
        counter = 0

        time_series_generate = TimeSeriesGeneration(self.simulator['start_date'] ,
                                                         self.simulator['start_date'] + timedelta(days=self.simulator['dataSize']))

        # time.sleep(20)
        for i in self.simulatorConfigs['dataset']:
            date_rng = time_series_generate.generate(i['frequency'])

            for j in i['components']:
                # check threading with sleep() function

                seasonal_component = SeasonalComponent().add_daily(date_rng,
                                                                    j['frequency'],
                                                                    season_type=self.simulatorConfigs['timeSeries_type'])

                trend = [int(i) for i in i['trendCoef'].split()]
                trend_component = TrendComponent().addComponent(date_rng, trend, data_size=self.simulatorConfigs['dataSize'],
                                    data_type=self.simulatorConfigs['timeSeries_type'])

                cyclic_component = CyclesComponent().addComponent(date_rng, i['cycle_frequency'],
                                                                       season_type=self.simulatorConfigs['dataSize'])

                if self.simulatorConfigs['dataSize'] == 'multiplicative':
                    data = seasonal_component *  trend_component * cyclic_component
                else:
                    data = seasonal_component + trend_component + cyclic_component

                # Create a MinMaxScaler instance
                scaler = MinMaxScaler(feature_range=(-1, 1))
                data = scaler.fit_transform(data.values.reshape(-1, 1))

                data = NoiseComponent.addComponent(data, i['noiseLevel'])

                data, anomaly = OutliersComponent.addComponent(data, i['outlierPercent'])

                data = MissingValuesComponent.addComponent(data, i['missingPercent'])

                df = pd.DataFrame({'value': data, 'timestamp': date_rng, 'anomaly': anomaly})
                # producer = ProducerFactory().createProducer(fileName , 'csv')
                # df.to_csv('sample_datasets/' + str(counter) + '.csv', encoding='utf-8', index=False)
                counter +=1
                fileName = i['id']+"_"+j['id'] + '.csv'
                producer = ProducerFactory().createProducer(fileName , 'csv')
                producer.saveData(df,fileName)
                meta_data.append({'simulator':self.simulatorConfigs['id'],
                                      'dataConfig':i['id'],
                                      'components':j['id'],
                                     'fileName': fileName,})


        meta_data_df = pd.DataFrame.from_records(meta_data)
        # print(simulator['startDate'])
        meta_data_name = 'sample_datasets/meta_data+'+self.simulatorConfigs['id']+'.csv'
        producer.saveData(meta_data_df , meta_data_name)
        SimulateController().update_meta(self.simulatorConfigs['id']  ,meta_data_name )
        SimulateController().update_proccess(self.simulatorConfigs['id'] , 0)
        SimulateController().update_status(self.simulatorConfigs['id'] , "Success")
        return  Response({'message':" building simulator: "+str(self.simulatorConfigs['id'])+" successfully "})
        
