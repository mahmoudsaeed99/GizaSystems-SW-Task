
from DataProducer.ProducerFactory import *
from DataProducer.CSVProducer import CSVProducer
import unittest

class TestProducerFactor(unittest.TestCase):

    # def setUp(self) -> None:
    #     self.file = fileFactor().createFile("xyz.csv")

    def test_get_object_success(self):
        fileName = 'xyz.csv'
        file = ProducerFactory().createProducer(fileName , 'csv')
        self.assertIsInstance(file , CSVProducer)

    def test_get_object_failure(self):
        fileName = 'xyz'
        # file = fileFactor().createFile(fileName)
        with self.assertRaises(Exception):
            file = ProducerFactory().createProducer(fileName,'')

        # self.assertIsInstance(fileName , CSVFile)    


testProd = TestProducerFactor()
testProd.test_get_object_success()
