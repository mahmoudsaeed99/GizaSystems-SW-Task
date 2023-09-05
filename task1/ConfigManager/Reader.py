
from abc import ABC , abstractmethod

class Reader(ABC):

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def read(self):
        pass

    