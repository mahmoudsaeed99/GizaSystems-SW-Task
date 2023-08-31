
from ConfigManager.fileFactor import fileFactor
from ConfigManager.CSVFile import CSVFile
import unittest

class TestFileFactor(unittest.TestCase):

    # def setUp(self) -> None:
    #     self.file = fileFactor().createFile("xyz.csv")

    def test_get_object_success(self):
        fileName = 'xyz.csv'
        file = fileFactor().createFile(fileName)
        self.assertIsInstance(file , CSVFile)

    def test_get_object_failure(self):
        fileName = 'xyz'
        # file = fileFactor().createFile(fileName)
        with self.assertRaises(Exception):
            file = fileFactor().createFile(fileName)

        # self.assertIsInstance(fileName , CSVFile)    



t = TestFileFactor()
# t.setUp()
# print(t.test_get_object_success())
t.test_get_object_failure()

