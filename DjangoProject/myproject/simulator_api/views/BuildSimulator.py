from .ComponentController import *

from sklearn.preprocessing import MinMaxScaler

from .TimeGeneration import TimeSeriesGeneration
# from .ConfigManager.ConfigManager import *
# import Components.AdditionalComponent
from .Components.CyclesComponent import *
from .Components.MissingValuesComponent import *
from .Components.NoiseComponent import *
from .Components.OutliersComponent import *
from .Components.SeasonalComponent import *
from .Components.TrendComponent import *
from .DataProducer.ProducerFactory import *
import threading


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

        if self.simulatorConfigs['endDate'] == '':
            endDate = self.simulatorConfigs['startDate'] + timedelta(days=self.simulatorConfigs['dataSize'])
        else:
            endDate = self.simulatorConfigs['endDate']

        time_series_generate = TimeSeriesGeneration(self.simulatorConfigs['startDate'] ,endDate)

        # time.sleep(20)
        for i in self.simulatorConfigs['dataset']:
            date_rng = time_series_generate.generate(i['frequency'])

            for j in i['components']:
                # check threading with sleep() function

                seasonal_component = SeasonalComponent().add_component(date_rng,j['multiplier'],
                                                                    j['frequency'],j['amplitude'],j['phase_shift'],
                                                                    self.simulatorConfigs['timeSeries_type'])

                trend = [int(i) for i in i['trendCoef'].split()]
                trend_component = TrendComponent().addComponent(date_rng, trend)

                cyclic_component = CyclesComponent().addComponent( i['cycle_frequency'],i['cycle_amplitude'],
                                                                       date_rng)

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
                fileName = "E:/SW/GizaSystems-SW-Task/DjangoProject/myproject/dataSet/"+str(i['id'])+"_"+str(j['id']) + '.csv'
                producer = ProducerFactory().createProducer(fileName , 'csv')
                producer.saveData(df,fileName)
                meta_data.append({'simulator':self.simulatorConfigs['id'],
                                      'dataConfig':i['id'],
                                      'components':j['id'],
                                     'fileName': fileName,})


        meta_data_df = pd.DataFrame.from_records(meta_data)
        # print(simulator['startDate'])
        meta_data_name = 'E:/SW/GizaSystems-SW-Task/DjangoProject/myproject/metaData/+'+str(self.simulatorConfigs['id'])+'.csv'
        producer.saveData(meta_data_df , meta_data_name)
        SimulateController().update_meta(self.simulatorConfigs['id']  ,meta_data_name )
        SimulateController().update_proccess(self.simulatorConfigs['id'] , 0)
        SimulateController().update_status(self.simulatorConfigs['id'] , "Success")
        return  Response({'message':" building simulator: "+str(self.simulatorConfigs['id'])+" successfully "})
        
