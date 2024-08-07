import os
import sys
import json
import pycocotools

class CocoHandler:

    def __init__(self) -> None:
        self.coco_dict = {
            "images" : [],
            "annotations" : [],
            "categories" : []
        }
        self.file_name_to_image_id = {}
        self.next_image_id = 1
        self.next_annotation_id = 1
        self.next_category_id = 1

    def get_or_create_image_entry(self, file_name: str, width: int, height: int) -> int:
        # If the image is not in the coco dict, add it and assign an id
        if not self.file_name_to_image_id[file_name]:
            assigned_id = self.next_category_id
            self.next_image_id += 1
            self.coco_dict["images"].append({
                "id" : assigned_id,
                "file_name" : file_name,
                "width" : width,
                "height" : height
                })
            self.file_name_to_image_id[file_name] = assigned_id

        # Return the id associated with the file_name
        return self.file_name_to_image_id[file_name]
        
        

