import unittest
import os
import sys

from src.toCocoConverter.CocoHandler import CocoHandler

current = os.path.dirname(os.path.realpath(__file__))
testFolder = os.path.dirname(current)
root = os.path.dirname(testFolder)
sys.path.append(os.path.join(root, "src"))

class CocoHandler_Tests(unittest.TestCase):

    def setUp(self):
        self.coco = CocoHandler()
        self.test_image_entry = {

        }

    def test_normal_runthrough(self):
        # Test image entries

        # Test it returns the correct id
        self.assertEqual(self.coco.get_or_create_image_entry("testfilename1.jpg", 100, 200), 1)
        img_validation_1 = {
            "id" : 1,
            "file_name" : "testfilename1.jpg",
            "width" : 100,
            "height" : 200
        }
        # Test it loaded the info correctly
        self.assertEqual(self.coco.coco_dict["images"][0], img_validation_1)

        # Repeat test on second image
        self.coco.get_or_create_image_entry("testfilename2.jpg", 300, 400)
        img_validation_2 = {
            "id" : 2,
            "file_name" : "testfilename2.jpg",
            "width" : 300,
            "height" : 400
        }
        self.assertEqual(self.coco.coco_dict["images"][1], img_validation_2)



        

