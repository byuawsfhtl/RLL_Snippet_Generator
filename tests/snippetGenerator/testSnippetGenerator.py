import unittest
import os
import io
from PIL import Image
import tarfile
import json
import sys
from io import StringIO

current = os.path.dirname(os.path.realpath(__file__))
testFolder = os.path.dirname(current)
root = os.path.dirname(testFolder)
sys.path.append(os.path.join(root, 'src'))
from SnippetGenerator import SnippetGenerator  # noqa: E402


class SnippetGenerator_Tests(unittest.TestCase):
    def setUp(self):
        self.image_tar_path = 'tests/resources/images.tar'
        self.json_tar_path = 'tests/resources/json.tar'
        self.test_tarfile_path = 'tests/resources/test.tar'
        self.test_image_tarfile_path = 'tests/resources/test_image.tar'
        self.instance = SnippetGenerator(self.image_tar_path, self.json_tar_path)
        self.test_text_data = 'This is not JSON data.'
        self.sample_image_path = 'tests/resources/sample_image.jpg'
        self.sample_image = Image.open(self.sample_image_path)
        # Create a sample JSON data and image for testing
        self.test_json_data = {
            'corners': [
                [[0, 0], [100, 0], [100, 100],
                 [0, 100], [100, 100], [100, 200]]
            ]
        }

    def tearDown(self):
        self.sample_image.close()

    def test_full_functionality(self):
        # Extract the json files from the json tar file
        self.instance.extract_json(self.json_tar_path)
        # Extract the image files from the image tar file
        for image, name in self.instance.image_from_tar_generator(self.image_tar_path):
            # get the expected names
            expected_names = self.get_names(name)
            i = 0
            # Using each image and its name, generate the snippets
            for snippet, snippet_name in self.instance.image_snippet_generator(image, name):
                assert snippet is not None
                self.assertEqual(snippet_name, expected_names[i])
                i += 1

    def test_make_snippets_pass(self):
        name = 'sample'
        self.instance.name_to_json[name] = self.test_json_data
        for snippet, name in self.instance.image_snippet_generator(self.sample_image, name):
            assert snippet is not None
            assert name is not None

    def get_names(self, name):
        json_data = self.instance.name_to_json[name]
        columns_and_rows = json_data['corners']
        names = []
        for i in range(len(columns_and_rows) - 2):
            for j in range(len(columns_and_rows[0]) - 1):
                # Create a name for the image
                names.append(name + '_row_' + str(j) + '_col_' + str(i) + '.png')
        return names

    def test_fail_make_snippets(self):
        # Redirect std out to catch print statements
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        name = 'sample'
        for snippet, name in self.instance.image_snippet_generator(self.sample_image, name):
            assert snippet is None
            assert name is None

        # Get the printed output
        printed_output = sys.stdout.getvalue()

        # Restore stdout
        sys.stdout = original_stdout

        expected_output = "Image sample not found in the json file\n"

        self.assertEqual(expected_output, printed_output)

    def test_extract_json_from_tarfile(self):
        # Create a sample tar file for testing
        with tarfile.open(self.test_tarfile_path, 'w') as tar:
            # Add a JSON file to the tarfile
            json_data_str = json.dumps(self.test_json_data)
            json_data_bytes = json_data_str.encode('utf-8')
            json_member = tarfile.TarInfo(name='sample.json')
            json_member.size = len(json_data_bytes)
            tar.addfile(json_member, fileobj=io.BytesIO(json_data_bytes))

        # Call the function to extract JSON data from the tarfile
        self.instance.extract_json(self.test_tarfile_path)

        # Test whether the data was correctly added to the dictionary
        self.assertIn('sample', self.instance.name_to_json)
        self.assertEqual(self.instance.name_to_json['sample'], self.test_json_data)

    # Test that it does not work when a different file is passed in
    def test_fail_extract_json_from_tarfile(self):
        # Redirect std out to catch print statements
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        # Create a sample tar file for testing with a non-JSON file
        with tarfile.open(self.test_tarfile_path, 'w') as tar:
            # Add a text file (not JSON) to the tarfile
            text_data_bytes = self.test_text_data.encode('utf-8')
            text_member = tarfile.TarInfo(name='text.txt')
            text_member.size = len(text_data_bytes)
            tar.addfile(text_member, fileobj=io.BytesIO(text_data_bytes))

            # Add a JSON file to the tarfile
            json_data_str = json.dumps(self.test_json_data)
            json_data_bytes = json_data_str.encode('utf-8')
            json_member = tarfile.TarInfo(name='sample.json')
            json_member.size = len(json_data_bytes)
            tar.addfile(json_member, fileobj=io.BytesIO(json_data_bytes))

        # Call the function to extract JSON data from the tarfile
        self.instance.extract_json(self.test_tarfile_path)

        # Get the printed output
        printed_output = sys.stdout.getvalue()

        # Restore stdout
        sys.stdout = original_stdout

        expected_output = "Wrong file type. File name was text. Please ensure that the tar includes only JSON files\n"

        # Check that the 'name_to_json' dictionary is empty (no JSON data was added)
        self.assertEqual(expected_output, printed_output)


if __name__ == '__main__':
    unittest.main()
