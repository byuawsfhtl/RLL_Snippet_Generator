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
        self.malformed_shape_warning = "WARNING:output_logger:Unsuccessful extraction on shape 3. Number of columns is 15 instead of 11, so this shape will be skipped. Extracted information:\n['test_reel_name_000.tar', 'test_image_name_000.jpg', 'Name Field', 1062.0833333333335, 227.16666666666669, 1062.0833333333335, 227.16666666666669, 394.375, 227.16666666666669, 394.375, 144.875, 1064.1666666666667, 140.70833333333334, 1065.2083333333335, 231.33333333333334]"
        self.df_columns = pd.Index(['reel_filename', 'image_filename', 'snip_name', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4'], dtype='object')
        self.df_row_0 = {'reel_filename': 'test_reel_name_000.tar', 'image_filename': 'test_image_name_000.jpg', 'snip_name': 'Card No.', 'x1': 71.45833333333337, 'y1': 205.29166666666669, 'x2': 70.41666666666669, 'y2': 141.75, 'x3': 304.7916666666667, 'y3': 143.83333333333334, 'x4': 308.95833333333337, 'y4': 210.5}
        self.df_len_rows = 110
        # Test correct output file to compare to

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
        with self.assertLogs("output_logger", "WARNING") as log:
            df = self.lm_converter.convert_to_dataframe(self.labelme_path, self.reel_name, self.image_name)
            # Assert the logger outputs a warning for a shape it can't read (incorrect number of points)
            self.assertIn(self.malformed_shape_warning, log.output)
            # Assert the created dataframe has the correct columns
            self.assertTrue(df.columns.equals(self.df_columns))
            # Assert the dataframe has the correct number of rows
            self.assertEqual(len(df), self.df_len_rows)
            # Assert the first row was created correctly
            self.assertEqual(df.iloc[0].to_dict(), self.df_row_0)

    def test_convert_to_tsv(self):
        pass
            
        
        




#converter = LabelMeConverter()
#df = converter.convert_to_dataframe(LABELME, REEL_NAME, IMAGE_NAME)
#print(df)


