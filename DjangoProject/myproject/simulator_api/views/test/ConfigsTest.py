import unittest
from ..DataConfig import *
from ...serializers import *


class ConfigsTest(unittest.TestCase):
        
    def getConfigs_success(self):
        dataConfig = {"frequency":"H1",
                        "trend_coefficients":"0 2 1 3",
                        "missing_percentage":0.06,
                        "outlier_percentage":10,
                        "noise_level":10,
                        "cycle_amplitude":0,
                        "cycle_frequency":1,
                    }
        configs = ConfigController().as_view()
        self.assertIsInstance(configs , ConfigSerializer)


config =   ConfigsTest()   
config.getConfigs_success()  

