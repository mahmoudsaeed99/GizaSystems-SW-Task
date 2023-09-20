from .DB import *
from ...models import *

import pandas as pd


class SQLDB(DB):

    def open(self):

        pass

    def read(self , Id):
        simulator = Simulator.objects.all().filter(id =Id)[0]
        configs = simulator.dataConfig.all()
        simulator = Simulator.objects.all().filter(id =Id).values()[0]
        dataset = []
        for i in range(len(configs)):
            component = configs[i].components.all().values()
            data = configs.values()[i]
            data['components'] = component
            dataset.append(data)
        # data = Simulator.objects.all().filter(id =Id)[0].dataconfig_set.all()[0].component_set.all()
        # configs = data.dataconfig_set.all()
        simulator['dataset'] = dataset
        # data = {
        #         'dataset': l,
        #         }
        return simulator


    
