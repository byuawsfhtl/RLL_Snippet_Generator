import unittest
import os
from snippet_generator import snippet_generator

class create_snippets_test(unittest.TestCase):
    def setUp(self):
        self.image_tar_path = 'C:/Users/gideo/Computer_Vision/Snippet_Generator/images.tar'
        self.json_tar_path = 'C:/Users/gideo/Computer_Vision/Snippet_Generator/json.tar'
        # self.name_to_json = dict()
        
    def test_make_snippets(self):
        self.instance = snippet_generator(self.image_tar_path, self.json_tar_path)
        self.assertTrue(os.path.exists(self.image_tar_path))
        self.assertTrue(os.path.exists(self.json_tar_path))
        
        self.instance.extract_json(self.json_tar_path)
        for image, name in self.instance.image_from_tar_generator(self.image_tar_path):
            print(name)
            for snippet, name in self.instance.image_snippet_generator(image, name):
               print(name)
        
        
        
        
        

if __name__ == '__main__':
    unittest.main()