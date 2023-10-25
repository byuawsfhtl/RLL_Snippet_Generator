import unittest
import os
import io
from snippet_generator import snippet_generator
from PIL import Image
import tarfile
import json
import sys
from io import StringIO

class create_snippets_test(unittest.TestCase):
    def setUp(self):
        self.image_tar_path = 'C:/Users/gideo/Computer_Vision/Snippet_Generator/images.tar'
        self.json_tar_path = 'C:/Users/gideo/Computer_Vision/Snippet_Generator/json.tar'
        self.test_tarfile_path  = "C:/Users/gideo/Computer_Vision/Snippet_Generator/test.tar"
        self.test_image_tarfile_path = "C:/Users/gideo/Computer_Vision/Snippet_Generator/test_image.tar"
        self.instance = snippet_generator(self.image_tar_path, self.json_tar_path)
        self.test_text_data = "This is not JSON data."
        self.sample_image_path = "C:/Users/gideo/Computer_Vision/Snippet_Generator/sample_image.jpg"
        self.sample_image = Image.open("C:/Users/gideo/Computer_Vision/Snippet_Generator/sample_image.jpg")
        # Create a sample JSON data and image for testing
        self.test_json_data = {
            'corners': [
                [[0, 0], [100, 0], [100, 100],
                [0, 100], [100, 100], [100, 200]]
            ]
        }
        
    
    def test_full_functionality(self):
        # Create a sample tar file for testing
        with tarfile.open(self.test_tarfile_path, 'w') as tar:
            # Add a JSON file to the tarfile
            json_data_str = json.dumps(self.test_json_data)
            json_data_bytes = json_data_str.encode('utf-8')
            json_member = tarfile.TarInfo(name='sample.json')
            json_member.size = len(json_data_bytes)
            tar.addfile(json_member, fileobj=io.BytesIO(json_data_bytes))
        
        # Add a sample image to the tarfile
        with tarfile.open(self.test_image_tarfile_path, 'w') as tar:
            image = Image.open(self.sample_image_path)
            image_bytes = image.tobytes()
            image_member = tarfile.TarInfo(name='sample.png')
            image_member.size = len(image_bytes)
            tar.addfile(image_member, fileobj=io.BytesIO(image_bytes))
            

        #Extract the json files from the json tar file
        self.instance.extract_json(self.json_tar_path)
        
        
        #Extract the image files from the image tar file
        for image, name in self.instance.image_from_tar_generator(self.image_tar_path):
            #Using each image and its name, generate the snippets
            for snippet, name in self.instance.image_snippet_generator(image, name):
                snippet.show()
                assert snippet is not None
                assert name is not None
                #Save the snippet
                snippet.save(name)
        
    def test_make_snippets_pass(self):
        name = 'sample'
        self.instance.name_to_json[name] = self.test_json_data
        for snippet, name in self.instance.image_snippet_generator(self.sample_image, name):
            assert snippet is not None
            assert name is not None
        
            
    def test_fail_make_snippets(self):
        #Redirect std out to catch print statements
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

    #Test that it does not work when a different file is passed in
    def test_fail_extract_json_from_tarfile(self):
        #Redirect std out to catch print statements
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