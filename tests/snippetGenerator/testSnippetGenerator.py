import unittest
import os
from PIL import Image
import sys

current = os.path.dirname(os.path.realpath(__file__))
testFolder = os.path.dirname(current)
root = os.path.dirname(testFolder)
sys.path.append(os.path.join(root, "src"))
from SnippetGenerator import SnippetGenerator  # noqa: E402


class SnippetGenerator_Tests(unittest.TestCase):
    def setUp(self):
        self.image_tar_path = "tests/resources/iowa_image.tar"
        self.json_tar_path = "tests/resources/iowa_json.tar"
        self.test_image_tarfile_path = "tests/resources/test_image.tar"
        self.instance = SnippetGenerator(self.image_tar_path, self.json_tar_path)
        self.test_text_data = "This is not JSON data."
        self.sample_image_path = "tests/resources/sample_image.jpg"

        self.sample_image = Image.open(self.sample_image_path)
        # Create a sample JSON data and image for testing
        self.test_json_data = {
            "corners": [
                [[0, 0], [100, 0], [100, 100], [0, 100], [100, 100], [100, 200]]
            ]
        }

    def tearDown(self):
        self.instance = None
        self.sample_image.close()
        directory = "tests/resources/output"
        # List all files in the directory
        if not os.path.exists(directory):
            return
        files = os.listdir(directory)
        # Iterate over each file and remove it
        for file_name in files:
            file_path = os.path.join(directory, file_name)
            try:
                # Attempt to remove the file
                os.remove(file_path)
                print("File '{}' successfully removed.".format(file_path))
            except OSError as e:
                # If file deletion fails, print the error message
                print("Error: {} - {}".format(e.filename, e.strerror))
        os.rmdir("tests/resources/output")

    def test_full_functionality(self):
        # Extract the json files from the json tar file
        self.instance.extract_json(self.json_tar_path)
        output_dir = "tests/resources/output"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        # Extract the image files from the image tar file
        for image, name in self.instance.image_from_tar_generator(self.image_tar_path):
            i = 0
            # Using each image and its name, generate the snippets
            for snippet, snippet_name in self.instance.image_snippet_generator(
                image, name
            ):
                assert snippet is not None

                # self.assertEqual(snippet_name, expected_names[i])
                image_filename = snippet_name
                output_path = os.path.join(output_dir, image_filename)
                snippet.save(output_path)
                i += 1
        # Check that the output directory contains the expected number of images
        self.assertEqual(len(os.listdir(output_dir)), 50)

    def test_name_not_in_json(self):
        with self.assertRaises(ValueError):
            for snippet, snippet_name in self.instance.image_snippet_generator(
                self.sample_image, "not_in_json"
            ):
                pass

    def test_image_not_in_tar(self):
        with self.assertRaises(ValueError):
            for image, name in self.instance.image_from_tar_generator(
                self.json_tar_path
            ):
                pass

    def test_fail_make_snippets(self):
        # Redirect std out to catch print statements
        name = "sample"
        with self.assertRaises(ValueError):
            for snippet, name in self.instance.image_snippet_generator(
                self.sample_image, name
            ):
                assert snippet is None
                assert name is None


if __name__ == "__main__":
    unittest.main()
