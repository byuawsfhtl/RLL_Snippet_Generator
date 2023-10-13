'''
This script takes an image and image directory files from a tarfile and a directory of json files that came from those images.
It links the json to the images via a map.
It then opens each image and creates snippets of the image based on the corner points in the json file. 
'''

from PIL import Image
import os
import json
import io
import numpy as np
import tarfile as tf
import csv
import cv2

class create_snippets():
    
    image_tar_path = 'V:/RA_work_folders/Gideon_Jardine/Snippet_Generator/images.tar'
    json_tar_path = 'V:/RA_work_folders/Gideon_Jardine/Snippet_Generator/json.tar'
    #global variables
    name_to_json = dict()

    #Constructor for this class
    def __init__(self): # Constructor
        pass

    def case_is_tar_file(self, input_path):
        tar_buffer = io.BytesIO()
        set_of_img_extensions = {'png', 'jpg', 'jpeg', 'jp2', 'tif', 'tiff'}
        with tf.open( input_path, mode='r') as tar_file:
            for member in tar_file:
                type = member.name.split('.')[-1]
                name = member.name.split('.')[0]
                if member.isfile() and member.name.endswith('.json'):
                    json_data = tar_file.extractfile(member)
                    dict_with_corner_points = json.load(json_data)
                    self.name_to_json[name] = dict_with_corner_points
                    print(member)
            # with open(image_file, mode='w', newline='') as csv_1:
            #     writer = csv.writer(csv_1)
            #     for member in tar_file:
                if type in set_of_img_extensions and len(self.name_to_json) > 0:
                    if name in self.name_to_json:
                        img_data = np.asarray(bytearray(tar_file.extractfile(member).read()), dtype=np.uint8)
                                        
                        
                        # Decode the image data using OpenCV and append the resulting numpy array to the images list
                        #Works like Image.open(image)
                        img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
                        original_image = Image.open(img)
                        print(img)
 


    # for image_file in list_of_images:
    #     image_path = os.path.join(input_image_dir, image_file)
    #     image_file_no_ext = image_file.split('.')[0]
    #     if image_file_no_ext not in dict_of_image_and_json_paths:
    #         dict_of_image_and_json_paths[image_file_no_ext] = []
    #         dict_of_image_and_json_paths[image_file_no_ext].append(image_path)


    def open_file(self, mode): # Open the tsv/csv_file
        return open(self.get_file(), mode, newline='')
    

    def make_snippets(self, image_and_json_path, dict_of_image_and_json_paths):
        for image_and_json_path in dict_of_image_and_json_paths.values():
            if len(image_and_json_path) != 2:
                print(f'Here\'s what\'s missing: {image_and_json_path}')
            else:
                image_path = image_and_json_path[0]
                json_path = image_and_json_path[-1]


                # Get the json object
                with open(json_path, 'r') as json_in:
                    dict_with_corner_points = json.load(json_in)
                
                # Get the corners
                columns_and_rows = dict_with_corner_points['corners']
                
                # Load the image
                original_image = Image.open(image_path)
                
                for i in range(len(columns_and_rows)-2):
                    
                    for j in range(len(columns_and_rows[0])-1):
                        
                        if (i > 33) and (j > 48):
                            print('stop here')

                        left_top_corner = columns_and_rows[i][j]
                        right_top_corner = columns_and_rows[i+1][j]
                        bottom_right_corner = columns_and_rows[i+1][j+1]
                        bottom_left_corner = columns_and_rows[i][j+1]

                        left_side = min(left_top_corner[0], bottom_left_corner[0]) 
                        upper_side = min(left_top_corner[1], right_top_corner[1])
                        right_side = max(bottom_right_corner[0], right_top_corner[0])
                        lower_side = max(bottom_right_corner[1], bottom_left_corner[1]) + 3

                        # Crop the image
                        cropped_image = original_image.crop((left_side, upper_side, right_side, lower_side))

                        # Create a name for the image 
                        cropped_image_name = image_path.split('.')[0].split('/')[-1] + '_row_' + str(j) + '_col_' + str(i) + '.png'

                        # Create a path to the cropped image
                        #cropped_image_path = os.path.join(output_snippet_dir, cropped_image_name)

                        # To save the cropped image
                        #cropped_image.save(cropped_image_path)

    def main(self):
        with self.open_file('r') as tar:
            json_file = self.json_tar_path 
        list_of_jsons = self.case_is_tar_file(json_file)
        
        for json_file in list_of_jsons:
            json_path = os.path.join(input_json_dir, json_file)
            json_file_no_ext = json_file.split('.')[0]
            if json_file_no_ext not in dict_of_image_and_json_paths:
                print('Something\'s wrong with your code, bud')
            else:
                self.dict_of_image_and_json_paths[json_file_no_ext].append(json_path)
        