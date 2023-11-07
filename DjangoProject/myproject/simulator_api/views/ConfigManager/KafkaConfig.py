
from .File import File
import yaml
from decouple import config

class KafkaConfig(File):
    def __init__(self, config_file):
        self.config_file = config_file
        self.open()

    def open(self):
        if self.config_file.endswith('.env'):
            config.read(self.config_file)
        elif self.config_file.endswith('.yml'):
            with open(self.config_file, 'r') as file:
                self.config = yaml.safe_load(file)
        pass
    def read(self , key):
        if self.config_file.endswith('.env'):
            return config(key)
        elif self.config_file.endswith('.yml'):
            return self.config.get(key)


