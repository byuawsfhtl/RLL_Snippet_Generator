import unittest
from .. import ProcessWordSnippets as Pws
import os


class ProcessWordSnippetsTests(unittest.TestCase):
    def setUp(self):
        self.image_tar_path = 'RLL_Snippet_Generator/tests/resources/images.tar'
        self.json_tar_path = 'RLL_Snippet_Generator/tests/resources/json.tar'
        self.snippets_tsv_path = 'RLL_Snippet_Generator/tests/resources/classificationTsv'
        self.output_dir = "RLL_Snippet_Generator/tests/aaaTestResults"
        self.no_path = "./not/a/valid_path"
        if os.path.exists(self.output_dir):
            raise Exception("If test results directory already exists, you must delete it manually to preform tests.")

    def test_ProcessWordSnippets_success(self):
        pws = Pws.ProcessWordSnippets()
        pws.process_word_snippets(self.snippets_tsv_path, self.image_tar_path, self.json_tar_path,
                                  self.output_dir)

    def test_ProcessWordSnippets_badPaths(self):
        pws = Pws.ProcessWordSnippets()
        self.assertRaises(Exception, pws.process_word_snippets, self.no_path, self.no_path, self.no_path,
                          self.output_dir)
