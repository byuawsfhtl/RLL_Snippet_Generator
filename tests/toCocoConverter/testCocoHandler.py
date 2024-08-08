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

        # TEST IMAGE ENTRIES

        # Test it returns the correct id
        self.assertEqual(self.coco.get_or_create_image_entry("testfilename1.jpg", 100, 200), 1, "Image entry did not return expected id")
        img_validation_1 = {
            "id" : 1,
            "file_name" : "testfilename1.jpg",
            "width" : 100,
            "height" : 200
        }
        # Test it loaded the info correctly
        self.assertEqual(self.coco.coco_dict["images"][0], img_validation_1, "Image data does not match expected values")

        # Repeat test on second image
        self.assertEqual(self.coco.get_or_create_image_entry("testfilename2.jpg", 300, 400), 2, "Image entry did not return expected id")
        img_validation_2 = {
            "id" : 2,
            "file_name" : "testfilename2.jpg",
            "width" : 300,
            "height" : 400
        }
        self.assertEqual(self.coco.coco_dict["images"][1], img_validation_2, "Image data does not match expected values")


        # TEST CATEGORY ENTRIES

        # Test first category entry

        # Test category id returned
        self.assertEqual(self.coco.get_or_create_category_entry("residence"), 1, "Category entry did not return expected id")
        # Test category data
        cat_validation_1 = {
            "id" : 1,
            "name" : "residence"
        }
        self.assertEqual(self.coco.coco_dict["categories"][0], cat_validation_1, "Category data does not match expected values")

        # Test second category entry
        self.assertEqual(self.coco.get_or_create_category_entry("occupation"), 2, "Category entry did not return expected id")
        cat_validation_2 = {
            "id" : 2,
            "name" : "occupation"
        }
        self.assertEqual(self.coco.coco_dict["categories"][1], cat_validation_2, "Category data does not match expected values")

        
        # TEST ANNOTATION ENTRIES

        # Test first annotation entry

        # Test id is returned correctly
        self.assertEqual(self.coco.create_annotation_entry(1, 2, [120, 92, 200, 235]), 1, "Annotation entry did not return expected id")
        # Test annotation data
        ann_validation_1 = {
            "id" : 1,
            "category_id" : 1,
            "image_id" : 2,
            "bbox" : [120, 92, 200, 235]
        }
        self.assertEqual(self.coco.coco_dict["annotations"][0], ann_validation_1, "Annotation data does not match expected values")

        # Test second annotation entry
        








        

