# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 14:49:09 2023

@author: Mahmoud Saeed
"""

from abc import ABC, abstractmethod
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class AdditionalComponent(ABC):

    def addComponent(self):
        pass
