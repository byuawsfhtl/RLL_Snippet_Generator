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

#from LabelMeConverter import LabelMeConverter

from src.LabelMeConverter import LabelMeConverter

class LabelMeConverter_Tests(unittest.TestCase):

    def setUp(self):
        # Test LabelMe file and some verification info
        self.labelme_path = os.path.join("tests", "resources", "iowa_labelme.json")
        self.labelme_shape_len = 111
        self.labelme_shape_0 = {'label': 'Card No.', 'points': [[71.45833333333337, 205.29166666666669], [70.41666666666669, 141.75], [304.7916666666667, 143.83333333333334], [308.95833333333337, 210.5]], 'group_id': None, 'shape_type': 'polygon', 'flags': {}}
        # Negative test files
        self.random_file_path = os.path.join("tests", "resources", "iowa_image.tar")
        self.empty_labelme_path = os.path.join("tests", "resources", "empty.json")
        self.no_shapes_labelme_path = os.path.join("tests", "resources", "no_shapes.json")
        # Negative path
        self.bad_path = os.path.join("tests", "resources", "non_existant_file.json")
        # Test reel and image names
        self.reel_name = "test_reel_name_000.tar"
        self.image_name = "test_image_name_000.jpg"
        # Create a LabelMeConverter
        self.lm_converter = LabelMeConverter()


    def test_read_in_shapes(self):
        # Test on a normal LabelMe file
        shapes = self.lm_converter.read_in_shapes(self.labelme_path)
        assert len(shapes) == self.labelme_shape_len
        assert shapes[0] == self.labelme_shape_0
        
        # Test on a non-JSON file
        with self.assertRaisesRegex(TypeError, "LabelMe file parameter extension is '.tar'; expected '.json'"):
            _ = self.lm_converter.read_in_shapes(self.random_file_path)
        
        # Test on a LabelMe file with an empty "shapes" list
        with self.assertRaisesRegex(ValueError, "Shapes list in LabelMe file is missing or empty"):
            _ = self.lm_converter.read_in_shapes(self.no_shapes_labelme_path)

        # Test on an empty JSON file
        with self.assertRaisesRegex(ValueError, r"^Opening or parsing the LabelMe file failed with this exception: .*"):
            _ = self.lm_converter.read_in_shapes(self.empty_labelme_path)

        # Test on a bad path
        with self.assertRaisesRegex(FileNotFoundError, f"LabelMe file does not exist: {self.bad_path}"):
            _ = self.lm_converter.read_in_shapes(self.bad_path)


        
    def test_convert_to_dataframe(self):
        self.lm_converter.convert_to_dataframe(self.labelme_path, self.reel_name, self.image_name)
        
        




#converter = LabelMeConverter()
#df = converter.convert_to_dataframe(LABELME, REEL_NAME, IMAGE_NAME)
#print(df)


