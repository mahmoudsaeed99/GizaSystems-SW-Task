# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 17:12:35 2023

@author: Mahmoud Saeed
"""

from .AdditionalComponent import *


class CyclesComponent(AdditionalComponent):
    
    
    def addComponent(data, cyclic_period, amplitude , data_size):
        """
        Add cyclic component to the time series data.

        Parameters:
            data (DatetimeIndex): The time index for the data.
            cyclic_periods (str): The type of cyclic periods ('No Cyclic Periods', 'Short Cycles', or 'Long Cycles').

        Returns:
            numpy.ndarray: The cyclic component of the time series.
        """

        return amplitude * np.sin(2 * np.pi * data_size.year / cyclic_period)
            # cycle_component += np.sin(2 * np.pi * (data.quarter-1) / 4)/
        # else:  # No Cyclic Periods
        #     cycle_component = 0 if season_type == 'additive' else 1
        #
        # return cycle_component
