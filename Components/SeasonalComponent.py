# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 16:58:51 2023

@author: Mahmoud Saeed
"""
from AdditionalComponent import *

class SeasonalComponent(AdditionalComponent):
    
   def addComponent(self, data, seasonality, season_type , type_ = 'daily'):
       """
       Add weekly seasonality component to the time series data.

       Parameters:
           data (DatetimeIndex): The time index for the data.
           seasonality (str): The type of seasonality ('Long', 'Short', or 'Intermediate').

       Returns:
           numpy.ndarray: The seasonal component of the time series.
       """
       # check add type like(`weekly` or `daily`)
       
       if type_.lower() == 'daily':
           season = 24
           season_data = data.hour
           
       elif type_.lower() == 'weekly':
           season = 7
           season_data = data.dayofweek
           
       if seasonality == "exist":  # Weekly Seasonality
           seasonal_component = np.sin(2 * np.pi * season_data / season)
           seasonal_component += 1 if season_type == 'multiplicative' else 0
       else:
           seasonal_component = np.zeros(len(data)) if season_type == 'additive' else np.ones(len(data))
       return pd.Series(seasonal_component)

