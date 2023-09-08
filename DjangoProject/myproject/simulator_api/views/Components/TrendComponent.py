# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 17:10:40 2023

@author: Mahmoud Saeed
"""
from .AdditionalComponent import *


class TrendComponent(AdditionalComponent):
    
    
    def addComponent(data, trend, data_size, data_type):
        """
        Add trend component to the time series data.

        Parameters:
            data (DatetimeIndex): The time index for the data.
            trend (str): The magnitude of the trend ('No Trend', 'Small Trend', 'Large Trend').

        Returns:
            numpy.ndarray: The trend component of the time series.
        """
        if trend == "exist":
            slope = random.choice([1, -1])
            trend_component = np.linspace(0, data_size / 30 * slope, len(data)) if slope == 1 else np.linspace(
                -1 * data_size / 30, 0, len(data))
        else:  # No Trend
            trend_component = np.zeros(len(data)) if data_type == 'additive' else np.ones(len(data))

        return pd.Series(trend_component)
