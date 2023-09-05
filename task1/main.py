# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 17:18:33 2023

@author: Mahmoud Saeed
"""
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from sklearn.preprocessing import MinMaxScaler

from TimeGeneration import TimeSeriesGeneration
from ConfigManager.ConfigManager import *
# import Components.AdditionalComponent
from Components.CyclesComponent import *
from Components.MissingValuesComponent import *
from Components.NoiseComponent import *
from Components.OutliersComponent import *
from Components.SeasonalComponent import *
from Components.TrendComponent import *
from DataProducer.ProducerFactory import *

random.seed(22)

def timeSeries():
    # Define simulation parameters
    #------------------new line-----------------
    configfile = ConfigManager().readConfig('xyz.csv' , 'csv')
    configData = configfile.read()
    #------------------------------------------
    start_date = datetime(2021, 7, 1)
    frequencies = ["1D", "10T", "30T", "1H", "6H", "8H"]  
    for i in range(len(configData)):
        data_size = random.choice(configData.iloc[i].data_sizes)
        freq = configData.iloc[i].frequencies
        start_date = configData.iloc[i].start_date
        time_series_generate = TimeSeriesGeneration(start_date , start_date + timedelta(days=data_size))
        date_rng = time_series_generate.generate(freq)
        # Create components
        daily_seasonality = configData.iloc[i].daily_seasonality_options
        daily_seasonal_component = SeasonalComponent().addComponent(date_rng,
                                                                    daily_seasonality,
                                                                    season_type=data_type)
        # daily_seasonal_component = add_daily_seasonality(date_rng, daily_seasonality,
        #                                                  season_type=data_type)
        weekly_seasonality = configData.iloc[i].weekly_seasonality
        weekly_seasonal_component = SeasonalComponent().addComponent(date_rng, daily_seasonality,
                                                         season_type=data_type ,type_='weekly')
        # weekly_seasonal_component = add_weekly_seasonality(date_rng, weekly_seasonality,
        #                                                    season_type=data_type)
        trend = configData.iloc[i].trend
        trend_component = TrendComponent().addComponent(date_rng, trend, data_size=data_size,
                                    data_type=data_type)
        
        # trend_component = add_trend(date_rng, trend, data_size=data_size,
        #                             data_type=data_type)
        cyclic_period = configData.iloc[i].cyclic_period
        cyclic_component = CyclesComponent().addComponent(date_rng, cyclic_period, season_type=data_type)
        
        if data_type == 'multiplicative':
            data = daily_seasonal_component * weekly_seasonal_component * trend_component * cyclic_component
        else:
            data = daily_seasonal_component + weekly_seasonal_component + trend_component + cyclic_component
        # Create a MinMaxScaler instance
        scaler = MinMaxScaler(feature_range=(-1, 1))
        data = scaler.fit_transform(data.values.reshape(-1, 1))
        noise_level = configData.iloc[i].noise_level
        data = NoiseComponent.addComponent(data, noise_level)
        # data = add_noise(data, noise_level)
        percentage_outliers = configData.iloc[i].percentage_outliers
        data, anomaly = OutliersComponent.addComponent(data, percentage_outliers)
        # data, anomaly = add_outliers(data, percentage_outliers)
        percentage_missing =configData.iloc[i].percentage_missing
        data = MissingValuesComponent.addComponent(data, 0.05)
        # data = add_missing_values(data, 0.05)

        # Save the data to a CSV file
        df = pd.DataFrame({'value': data, 'timestamp': date_rng, 'anomaly': anomaly})
        # df.to_csv('sample_datasets/' + str(counter) + '.csv', encoding='utf-8', index=False)
        fileName = str(counter) + '.csv'
        producer = ProducerFactory().createProducer(fileName , 'csv')
        producer.saveData(df,fileName)
        meta_data.append({'id': fileName,
                          'data_type': data_type,
                          'daily_seasonality': daily_seasonality,
                          'weekly_seasonality': weekly_seasonality,
                          'noise (high 30% - low 10%)': noise_level,
                          'trend': trend,
                          'cyclic_period (3 months)': cyclic_period,
                          'data_size': data_size,
                          'percentage_outliers': percentage_outliers,
                          'percentage_missing': 0.05,
                          'freq': freq})
        
        meta_data_df = pd.DataFrame.from_records(meta_data)
        producer.saveData(meta_data_df , 'sample_datasets/meta_data.csv')


if __name__ == "__main__":
    main()
