import unittest
import os
import sys
import pandas as pd

current = os.path.dirname(os.path.realpath(__file__))
testFolder = os.path.dirname(current)
root = os.path.dirname(testFolder)
sys.path.append(os.path.join(root, "src"))

#from LabelMeConverter import LabelMeConverter
from src.LabelMeConverter import LabelMeConverter

class LabelMeConverter_Tests(unittest.TestCase):
    '''
    This class tests the functions of the LabelMeConverter class. The tests are named after the corresponding functions in LabelMeConverter.py.
    '''

    def setUp(self):
        # Test LabelMe file path
        self.labelme_path = os.path.join("tests", "resources", "iowa_labelme.json")
        # Verification info for test LabelMe file (iowa_labelme.json)
        self.labelme_shape_len = 111
        self.labelme_shape_0 = {'label': 'Card No.', 'points': [[71.45833333333337, 205.29166666666669], [70.41666666666669, 141.75], [304.7916666666667, 143.83333333333334], [308.95833333333337, 210.5]], 'group_id': None, 'shape_type': 'polygon', 'flags': {}}
        self.malformed_shape_warning = "WARNING:output_logger:Unsuccessful extraction on shape 3. Number of columns is 15 instead of 11, so this shape will be skipped. Extracted information:\n['test_reel_name_000.tar', 'test_image_name_000.jpg', 'Name Field', 1062.0833333333335, 227.16666666666669, 1062.0833333333335, 227.16666666666669, 394.375, 227.16666666666669, 394.375, 144.875, 1064.1666666666667, 140.70833333333334, 1065.2083333333335, 231.33333333333334]"
        self.df_columns = pd.Index(['reel_filename', 'image_filename', 'snip_name', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4'], dtype='object')
        self.df_row_0 = {'reel_filename': 'test_reel_name_000.tar', 'image_filename': 'test_image_name_000.jpg', 'snip_name': 'Card No.', 'x1': 71.45833333333337, 'y1': 205.29166666666669, 'x2': 70.41666666666669, 'y2': 141.75, 'x3': 304.7916666666667, 'y3': 143.83333333333334, 'x4': 308.95833333333337, 'y4': 210.5}
        self.df_len_rows = 110
        # Test output directory (just goes to resources)
        self.output_directory = os.path.join("tests", "resources")
        self.output_file_path = os.path.join("tests", "resources", "iowa_labelme.tsv")
        # Output file verification info
        # Note - the correct output for iowa_labelme.json is available at resources/correct_LabelMeConverter_output.tsv
        self.output_expected_size = 20169
        # Negative test files
        self.random_file_path = os.path.join("tests", "resources", "iowa_image.tar")
        self.empty_labelme_path = os.path.join("tests", "resources", "empty.json")
        self.no_shapes_labelme_path = os.path.join("tests", "resources", "no_shapes.json")
        # Negative path
        self.bad_path = os.path.join("tests", "resources", "non_existant_file.json")
        # Test reel and image names
        self.reel_filename = "test_reel_name_000.tar"
        self.image_filename = "test_image_name_000.jpg"
        # Create a LabelMeConverter
        self.lm_converter = LabelMeConverter()


    def test_read_in_shapes(self):
        # Test read_in_shapes() on a normal LabelMe file
        shapes = self.lm_converter.read_in_shapes(self.labelme_path)
        self.assertEqual(len(shapes), self.labelme_shape_len, "Incorrect number of shapes were parsed")
        self.assertEqual(shapes[0], self.labelme_shape_0, "Test shape, shapes[0], does not match expected value")
        
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
            # Call convert_to_dataframe()
            df = self.lm_converter.convert_to_dataframe(self.labelme_path, self.reel_filename, self.image_filename)
            # Assert the logger outputs a warning for a shape it can't read (incorrect number of points)
            self.assertIn(self.malformed_shape_warning, log.output, "Malformed shape did not trigger an error message from the logger")
            # Assert the created dataframe has the correct columns
            self.assertTrue(df.columns.equals(self.df_columns), "Output dataframe has incorrect columns")
            # Assert the dataframe has the correct number of rows
            self.assertEqual(len(df), self.df_len_rows, "Output dataframe has incorrect number of rows")
            # Assert the first row was created correctly
            self.assertEqual(df.iloc[0].to_dict(), self.df_row_0, "df[0] does not match expected row")

    def test_convert_to_tsv(self):
        # Call convert_to_tsv()
        self.lm_converter.convert_to_tsv(self.labelme_path, self.reel_filename, self.image_filename, self.output_directory)
        # Check if file exists
        self.assertTrue(os.path.exists(self.output_file_path), "Output file was not created (or saved at an unexpected path)")
        # Check that file is about the right size
        self.assertAlmostEqual(os.path.getsize(self.output_file_path), self.output_expected_size, msg="Output file size differs from the expected size by more than 20 bytes", delta=20)
    
    def tearDown(self):
        # Remove the test output file (if it was created)
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)

