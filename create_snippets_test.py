import unittest
import os
from create_snippets import create_snippets

class create_snippets_test(unittest.TestCase):
    def setUp(self):
        self.image_tar_path = 'V:/RA_work_folders/Gideon_Jardine/Snippet_Generator/images.tar'
        self.json_tar_path = 'V:/RA_work_folders/Gideon_Jardine/Snippet_Generator/json.tar'
        self.instance = create_snippets
        self.name_to_json = dict()
        
    def test_make_snippets(self):
        self.assertTrue(os.path.exists(self.image_tar_path))
        self.assertTrue(os.path.exists(self.json_tar_path))
        
        self.instance.case_is_tar_file(self, self.json_tar_path)
        self.instance.case_is_tar_file(self, self.image_tar_path)

if __name__ == '__main__':
    unittest.main()