# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 17:10:40 2023

@author: Mahmoud Saeed
"""
from .AdditionalComponent import *


class TrendComponent(AdditionalComponent):
    
    
    def addComponent(self , data, trend_coef,):
        """
        Add trend component to the time series data.

        Parameters:
            data (DatetimeIndex): The time index for the data.
            trend (str): The magnitude of the trend ('No Trend', 'Small Trend', 'Large Trend').

        Returns:
            numpy.ndarray: The trend component of the time series.
        """
        if len(trend_coef) == 0:
            return np.zeros(len(data))
        trend = 0
        for i, coefficient in enumerate(trend_coef):
            time_intervals = np.arange(len(data))
            trend += coefficient * time_intervals ** i

        return trend
