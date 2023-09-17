# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 17:15:16 2023

@author: Mahmoud Saeed
"""
from .AdditionalComponent import *


class NoiseComponent(AdditionalComponent):
    
    def addComponent(data, noise_level):
        """
        Add noise component to the time series data.

        Parameters:
            data (DatetimeIndex): The time index for the data.
            noise_level (str): The magnitude of noise ('No Noise', 'Small Noise', 'Intermediate Noise', 'Large Noise').

        Returns:
            numpy.ndarray: The noise component of the time series.
        """
        signal_power = np.var(data)

        # Step 2: Determine the Desired SNR (in dB)
        desired_snr_db = noise_level  # Desired SNR in dB

        # Step 3: Calculate the Noise Power (in dB and linear scale)
        noise_power_db = signal_power - desired_snr_db

        noise_power = 10 ** (noise_power_db / 10)

        # Step 4: Generate Noise with the Calculated Power
        noise_stddev = np.sqrt(noise_power)
        noise = np.random.normal(0, noise_stddev, len(data))

        return noise
        # if noise_level == "small":
        #     noise_level = 0.1
        #     # noise = np.random.normal(0, 0.05, len(data))
        # elif noise_level == "large":
        #     noise_level = 0.3
        #     # noise = np.random.normal(0, 0.1, len(data))
        # else:  # No Noise
        #     noise_level = 0
        #
        # noise = np.zeros_like(data)
        # for i in range(len(data)):
        #     noise[i] = np.random.normal(0, abs(data[i]) * noise_level) if noise_level > 0 else 0
        # return pd.Series((data + noise)[:, 0])
