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
from DataProducer.CSVProducer import*

random.seed(22)


def main():
    # Define simulation parameters
    #------------------new line-----------------
    configData = ConfigManager().readConfig('xyz.csv')
    #------------------------------------------
    start_date = datetime(2021, 7, 1)
    frequencies = ["1D", "10T", "30T", "1H", "6H", "8H"]
    # daily_seasonality_options = ["no", "exist"]
    # weekly_seasonality_options = ["exist", "no"]
    # noise_levels = ["small"]  # , "large"]
    # trend_levels = ["exist", "no"]
    # cyclic_periods = ["exist", "no"]
    # data_types = [""
    #               "", "additive"]
    # percentage_outliers_options = [0.05]  # , 0]
    # data_sizes = [60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 365]
    meta_data = []
    data
    counter = 0
    # for freq in frequencies:
    for daily_seasonality in configData.daily_seasonality_options:
        for weekly_seasonality in configData.weekly_seasonality_options:
            for noise_level in configData.noise_levels:
                for trend in configData.trend_levels:
                    for cyclic_period in configData.cyclic_periods:
                        for percentage_outliers in configData.percentage_outliers_options:
                            for data_type in configData.data_types:
                                for _ in range(16):
                                    # for data_size in data_sizes:
                                    data_size = random.choice(configData.data_sizes)
                                    freq = random.choice(frequencies)
                                    counter += 1
                                    file_name = f"TimeSeries_daily_{daily_seasonality}_weekly_{weekly_seasonality}_noise_{noise_level}_trend_{trend}_cycle_{cyclic_period}_outliers_{int(percentage_outliers * 100)}%_freq_{freq}_size_{data_size}Days.csv"
                                    print(f"File '{file_name}' generated.")
                                    # Generate time index

                                    # ---------------------new line---------------------------
                                    time_series_generate = TimeSeriesGeneration(start_date , start_date + timedelta(days=data_size))
                                    date_rng = time_series_generate.generate(freq)
                                    # ------------------------------------------------

                                    # date_rng = generate_time_series(start_date, start_date + timedelta(days=data_size),
                                    #                                 freq)
                                    # Create components
                                    daily_seasonal_component = SeasonalComponent().addComponent(date_rng, daily_seasonality,
                                                                                     season_type=data_type)
                                    # daily_seasonal_component = add_daily_seasonality(date_rng, daily_seasonality,
                                    #                                                  season_type=data_type)
                                    weekly_seasonal_component = SeasonalComponent().addComponent(date_rng, daily_seasonality,
                                                                                     season_type=data_type ,type_='weekly')
                                    # weekly_seasonal_component = add_weekly_seasonality(date_rng, weekly_seasonality,
                                    #                                                    season_type=data_type)
                                    trend_component = TrendComponent().addComponent(date_rng, trend, data_size=data_size,
                                                                data_type=data_type)
                                    
                                    # trend_component = add_trend(date_rng, trend, data_size=data_size,
                                    #                             data_type=data_type)
                                    cyclic_period = "exist"
                                    cyclic_component = CyclesComponent().addComponent(date_rng, cyclic_period, season_type=data_type)

                                    # cyclic_component = add_cycles(date_rng, cyclic_period, season_type=data_type)

                                    # Combine components and add missing values and outliers
                                    if data_type == 'multiplicative':
                                        data = daily_seasonal_component * weekly_seasonal_component * trend_component * cyclic_component
                                    else:
                                        data = daily_seasonal_component + weekly_seasonal_component + trend_component + cyclic_component
                                    # Create a MinMaxScaler instance
                                    scaler = MinMaxScaler(feature_range=(-1, 1))
                                    data = scaler.fit_transform(data.values.reshape(-1, 1))
                                    data = NoiseComponent.addComponent(data, noise_level)
                                    # data = add_noise(data, noise_level)
                                    data, anomaly = OutliersComponent.addComponent(data, percentage_outliers)
                                    # data, anomaly = add_outliers(data, percentage_outliers)
                                    data = MissingValuesComponent.addComponent(data, 0.05)
                                    # data = add_missing_values(data, 0.05)

                                    # Save the data to a CSV file
                                    df = pd.DataFrame({'value': data, 'timestamp': date_rng, 'anomaly': anomaly})
                                    # df.to_csv('sample_datasets/' + str(counter) + '.csv', encoding='utf-8', index=False)
                                    fileName = str(counter) + '.csv'
                                    CVSProducer().saveData(df , 'sample_datasets/' + fileName) 
                                    """s
                                    import matplotlib.pyplot as plt
                                    plt.figure(figsize=(10, 6))
                                    # Plot the time series data
                                    plt.plot(df['timestamp'], df['value'], marker='o', linestyle='-', color='b',
                                             label='Time Series Data')
                                    # Add labels and title
                                    plt.xlabel('Time')
                                    plt.ylabel('Value')
                                    plt.title('Time Series Plot')
                                    plt.legend()
                                    # Display the plot
                                    plt.tight_layout()
                                    plt.show()
                                    break
                                    """

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
                                    # generate_csv(list(zip(date_rng, data)), file_name)

    meta_data_df = pd.DataFrame.from_records(meta_data)
    CSVProducer().saveData(meta_data_df , 'sample_datasets/meta_data.csv')
    # meta_data_df.to_csv('sample_datasets/meta_data.csv', encoding='utf-8', index=False)


if __name__ == "__main__":
    main()
