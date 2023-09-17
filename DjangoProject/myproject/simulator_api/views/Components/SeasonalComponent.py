# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 16:58:51 2023

@author: Mahmoud Saeed
"""
from .AdditionalComponent import *

class SeasonalComponent(AdditionalComponent):

    
   def add_component(self,data_range ,multiplier , freq , amplitude , phase_shift , seasonality):
    """
    Add seasonality component to the time series data.

    Parameters:
        data (DatetimeIndex): The time index for the data.
        seasonality (str): The type of seasonality ('Long', 'Short', or 'Intermediate').

    Returns:
        numpy.ndarray: The seasonal component of the time series.
    """
    _seasonality = {
            "Daily": amplitude * np.sin(
                2 * np.pi * ((data_range.hour + 1) / (24 * multiplier)) + phase_shift),
            "Weekly": amplitude * np.sin(
                2 * np.pi * (data_range.day / (7 * multiplier)) + phase_shift),
            "Monthly": amplitude * np.sin(
                2 * np.pi * (data_range.dayofyear / (30 * multiplier)) + phase_shift),
    }
    seasonal_component = _seasonality.get(freq)
    seasonal_component += 1 if seasonality == 'multiplicative' else 0
    return seasonal_component

    # if freq == "Weekly":  # Weekly Seasonality
    #     seasonal_component = 2 * np.pi * (data_range / (7 * multiplier)) + phase_shift)
    #     seasonal_component += 1 if seasonality == 'multiplicative' else 0
    # elif freq == "Daily":
    #     seasonal_component = np.sin(2 * np.pi * data_range.hour / 24)
    #     seasonal_component += 1 if seasonality == 'multiplicative' else 0
    # elif freq == "Monthly":
    #     seasonal_component = np.sin(2 * np.pi * data_range.dayofweek / 4)
    #     seasonal_component += 1 if seasonality == 'multiplicative' else 0
    # else:
    #     seasonal_component = np.zeros(len(data)) if season_type == 'additive' else np.ones(len(data))
    # return pd.Series(seasonal_component)
