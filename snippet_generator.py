'''
This script takes an image and image directory files from a tarfile and a directory of json files that came from those images.
It links the json to the images via a map.
It then opens each image and creates snippets of the image based on the corner points in the json file. 
'''

from PIL import Image
import os
import imghdr
import json
import io
import numpy as np
import tarfile as tf
import cv2


class snippet_generator():

    #Constructor for this class
    def __init__(self, tar1, tar2): # Constructor
        self.image_tar_path = tar1
        self.json_tar_path = tar2
        self.name_to_json = dict()
        self.image_names = set()
        
    def image_snippet_generator(self, image, name):
        if name in self.name_to_json:
            json_data = self.name_to_json[name]
            columns_and_rows = json_data['corners']
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
                    cropped_image = image.crop((left_side, upper_side, right_side, lower_side))

                    # Create a name for the image 
                    cropped_image_name = name + '_row_' + str(j) + '_col_' + str(i) + '.png'
                    
                    #Generate the snippet
                    yield cropped_image, cropped_image_name
        else:
            print(f"Image {name} not found in the json file")
                                
                                
    def image_from_tar_generator(self, image_path):
        set_of_img_extensions = {'png', 'jpg', 'jpeg', 'jp2', 'tif', 'tiff'}
        with tf.open( image_path, mode='r') as tar_file:
            # Iterate through each member of the tarfile
            for member in tar_file:
                type = member.name.split('.')[-1]
                name = member.name.split('.')[0]
                if name in self.image_names:
                    continue
                # If it is an image decode it and create the snippets
                if type in set_of_img_extensions and len(self.name_to_json) > 0:
                    #Check if the image name is in the json file
                    if name in self.name_to_json:
                        # Extract the image data from the tarfile
                        img_data = np.asarray(bytearray(tar_file.extractfile(member).read()), dtype=np.uint8)
                        
                        # Decode the image file
                        cv2_image = cv2.imdecode(img_data, cv2.IMREAD_COLOR)

                        if cv2_image is not None:
                            #Create an Image
                            original_image = Image.fromarray(cv2_image)
                            
                            self.image_names.add(name)                       

                            yield original_image, name 
                        else:
                            # Image decoding failed
                            print(f"cv2_image {name} is None. Image decoding failed.")            
 
                                        
                        

                else:
                    print(f"Wrong file type. File was {name}. Please ensure that the tar includes only image files")                    
                        

    def extract_json(self, input_path):
        with tf.open( input_path, mode='r') as tar_file:
            # Iterate through each member of the tarfile
            for member in tar_file:
                name = member.name.split('.')[0]
                # If it is a json file extract it and store it in a dictionary
                if member.isfile() and member.name.endswith('.json'):
                    json_data = tar_file.extractfile(member)
                    dict_with_corner_points = json.load(json_data)
                    self.name_to_json[name] = dict_with_corner_points
                    # print(member)
                else:
                    print(f"Wrong file type. File name was {name}. Please ensure that the tar includes only JSON files")

    
        