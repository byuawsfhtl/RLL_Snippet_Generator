import unittest
import os
import sys

from src.toCocoConverter.ToCocoConverter import ToCocoConverter

current = os.path.dirname(os.path.realpath(__file__))
testFolder = os.path.dirname(current)
root = os.path.dirname(testFolder)
sys.path.append(os.path.join(root, "src"))

class ToCocoConverter_Tests(unittest.TestCase):

    def setUp(self):
        self.coco_converter = ToCocoConverter()
        self.input_path = os.path.join("tests", "resources", "iowa.tsv")

    
    