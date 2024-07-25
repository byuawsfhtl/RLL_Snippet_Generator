import unittest
import os
import sys
import json
import argparse
import pandas as pd

# TODO: figure out how to fix the import...
current = os.path.dirname(os.path.realpath(__file__))
testFolder = os.path.dirname(current)
root = os.path.dirname(testFolder)
sys.path.append(os.path.join(root, "src"))

from LabelMeConverter import LabelMeConverter

class LabelMeConverter_Tests(unittest.TestCase):

    def setUp(self):
        self.labelme_path = os.path.join("tests", "resources", "iowa_labelme.json")
        self.random_file_path = os.path.join("tests", "resources", "iowa_labelme.json")
        self.reel_name = "test_reel_name_000.tar"
        self.image_name = "test_image_name_000.jpg"
        self.lm_converter = LabelMeConverter()


    def test_read_in_shapes(self):
        self.lm_converter.read_in_shapes(self.labelme_path)




converter = LabelMeConverter()
df = converter.convert_to_dataframe(LABELME, REEL_NAME, IMAGE_NAME)
print(df)


