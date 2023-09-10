# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 16:58:51 2023

@author: Mahmoud Saeed
"""
from .AdditionalComponent import *

class SeasonalComponent(AdditionalComponent):
    
   def add_component(data, seasonality, season_type):
    """
    Add seasonality component to the time series data.

    Parameters:
        data (DatetimeIndex): The time index for the data.
        seasonality (str): The type of seasonality ('Long', 'Short', or 'Intermediate').

    Returns:
        numpy.ndarray: The seasonal component of the time series.
    """
    if seasonality == "Weekly":  # Weekly Seasonality
        seasonal_component = np.sin(2 * np.pi * data.dayofweek / 7)
        seasonal_component += 1 if season_type == 'multiplicative' else 0
    elif seasonality == "Daily":
        seasonal_component = np.sin(2 * np.pi * data.hour / 24)
        seasonal_component += 1 if season_type == 'multiplicative' else 0
    elif seasonality == "Monthly":
        seasonal_component = np.sin(2 * np.pi * data.dayofweek / 4)
        seasonal_component += 1 if season_type == 'multiplicative' else 0
    else:
        seasonal_component = np.zeros(len(data)) if season_type == 'additive' else np.ones(len(data))
    return pd.Series(seasonal_component)