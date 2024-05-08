import unittest
import os
import sys
import shutil

current = os.path.dirname(os.path.realpath(__file__))
testFolder = os.path.dirname(current)
root = os.path.dirname(testFolder)
sys.path.append(os.path.join(root, "src"))
import ProcessWordSnippets as Pws  # noqa: E402


class ProcessWordSnippetsTestss(unittest.TestCase):
    def setUp(self):
        self.image_tar_path = "tests/resources/iowa_image.tar"
        self.json_tar_path = "tests/resources/iowa_json.tar"
        self.snippets_tsv_path = "tests/resources/classificationTsv"
        self.output_dir = "tests/aaaTestResults"
        self.no_path = "./not/a/valid_path"
        if os.path.exists(self.output_dir):
            print("Results directory already exists. Deleting.")
            shutil.rmtree(self.output_dir)

    def test_ProcessWordSnippets_success(self):
        pws = Pws.ProcessWordSnippets()
        pws.process_word_snippets(
            self.snippets_tsv_path,
            self.image_tar_path,
            self.json_tar_path,
            self.output_dir,
        )

    def test_ProcessWordSnippets_badPaths(self):
        pws = Pws.ProcessWordSnippets()
        self.assertRaises(
            Exception,
            pws.process_word_snippets,
            self.no_path,
            self.no_path,
            self.no_path,
            self.output_dir,
        )


if __name__ == "__main__":
    unittest.main()
