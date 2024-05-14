"""
This file contains the SnippetGenerator class which is used to crop snippets out of images.
"""

import tarfile
import io
import pandas as pd
import math
import os
from PIL import Image
from typing import Tuple


class CustomException(Exception):
    """A custom exception class. Used to identify error with our scripts."""

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"



class SnippetGenerator:
    """
    This class generates image snippets from a tar file containing images
    and a pandas dataframe that contains coordinate information for the snippets. 
    """

    # Constructor for this class
    def __init__(self, df: pd.DataFrame):
        """
        Initializes the snippet_generator class with the paths to the tar files containing images and json files.

        Args:
        df: A DataFrame object that contains at least the following information: reel_filename, image_filename, snip_name, x1, y1, ... x4, y4
        """
        self.map_coordinates_to_images = self.convert_df_to_map(df)


    def convert_df_to_map(self, df: pd.DataFrame):
        dict_of_reel_image_field_to_coordinates = {}

        for index, row in df.iterrows():
            try:
                reel_filename, image_filename, snip_name, box_coordinates = self.get_info_from_dataframe_row(row)

                if reel_filename in dict_of_reel_image_field_to_coordinates:
                    self.check_if_imageid_in_dict(dict_of_reel_image_field_to_coordinates, reel_filename, image_filename, snip_name, box_coordinates)
                else:
                    dict_of_reel_image_field_to_coordinates[reel_filename] = {}
                    self.check_if_imageid_in_dict(dict_of_reel_image_field_to_coordinates, reel_filename, image_filename, snip_name, box_coordinates)
            except CustomException as e:
                print("Found error: ", e)

        return dict_of_reel_image_field_to_coordinates


    def get_info_from_dataframe_row(self, row):
        if any(self.check_for_errors(x) for x in row):
            raise CustomException(f"None or Nan values found in dataframe at row: {row['reel_filename']}, {row['image_filename']}, {row['snip_name']}")
        else:
            reel_filename, image_filename, snip_name = row['reel_filename'], row['image_filename'], row['snip_name']
            box_coordinates = self.get_box_coordinates(row)
            return reel_filename, image_filename, snip_name, box_coordinates


    def check_for_errors(self, x):
        if isinstance(x, int) or isinstance(x, float) or isinstance(x, complex):
            if math.isnan(x):
                return True
        if x is None:
            return True


    def get_box_coordinates(self, row: pd.Series):
        x_coordinates = [row[f'x{i}'] for i in range(1, 5)]
        y_coordinates = [row[f'y{i}'] for i in range(1, 5)]

        left, upper, right, lower = min(x_coordinates), min(y_coordinates), max(x_coordinates), max(y_coordinates)

        return (left, upper, right , lower)
    

    def check_if_imageid_in_dict(self, dict_of_reel_image_field_to_coordinates, reel_filename, image_filename, field, box_coordinates):
        if image_filename in dict_of_reel_image_field_to_coordinates[reel_filename]:
            self.add_field_and_coordinates(dict_of_reel_image_field_to_coordinates, reel_filename, image_filename, field, box_coordinates)
        else:
            dict_of_reel_image_field_to_coordinates[reel_filename][image_filename] = []
            self.add_field_and_coordinates(dict_of_reel_image_field_to_coordinates, reel_filename, image_filename, field, box_coordinates)
            

    def add_field_and_coordinates(self, dict_of_reel_image_field_to_coordinates, reel_filename, image_filename, field, box_coordinates):
        dict_of_reel_image_field_to_coordinates[reel_filename][image_filename].append((field, box_coordinates))


    def save_snippets_to_directory(self, input_tarfile: str, output_directory: str, batch_size: int = 10000):
        for snippets, snippet_names in self.get_batch_of_snippets(input_tarfile, batch_size):
                for snippet_name, snippet in zip(snippets, snippet_names):
                    tarfile_name, image_name = snippet_name.split('_')[:2]

                    first_directory = os.path.join(output_directory, tarfile_name)
                    second_directory = os.path.join(first_directory, image_name)
                    path_to_snippet = os.path.join(second_directory, snippet_name)

                    if not os.path.exists(first_directory):
                        os.makedirs(first_directory)
                        os.makedirs(second_directory)

                    if not os.path.exists(second_directory):
                        os.makedirs(second_directory)

                    snippet.save(path_to_snippet)

    
    def save_snippets_as_tar(self, input_tarfile: str, output_directory: str, batch_size: int = 10000):
        outfile_name = os.path.splitext(os.path.basename(input_tarfile))[0] + "_snippets.tar.gz"
        outfile_path = os.path.join(output_directory, outfile_name)

        with tarfile.open(outfile_path, "w:gz") as tar_out:
            for snippets, snippet_names in self.get_batch_of_snippets(input_tarfile, batch_size):
                for snippet_name, snippet in zip(snippets, snippet_names):
                    try:
                        snippet_byte_arr = io.BytesIO()
                        snippet.save(snippet_byte_arr, format="JPEG")
                        snippet_byte_arr.seek(0)

                        snippet_info = tarfile.TarInfo(name=snippet_name)
                        snippet_info.size = len(snippet_byte_arr.getvalue())

                        tar_out.addfile(snippet_info, snippet_byte_arr)
                    except Exception as e:
                        print(snippet_name)
                        print(e)
                tar_out.fileobj.flush()
        

    def get_batch_of_snippets(self, input_tarfile: str, batch_size: int):
        
        tarfile_name = os.path.basename(input_tarfile)

        snippets, snippet_names = [], []
        for image, image_name in self.yield_image_and_name(input_tarfile):
            for snippet_name, snippet in self.yield_snippet_and_name(tarfile_name, image_name, image):
                snippets.append(snippet)
                snippet_names.append(snippet_name)
                
                if len(snippets) == batch_size:
                    yield snippet_names, snippets
                    snippets, snippet_names = [], []
                    
        if snippets and snippet_names:
            yield snippet_names, snippets
                
    
    def yield_image_and_name(self, input_tarfile):

        read_param = "r"
        if ".gz" in os.path.basename(input_tarfile):
            read_param = "r:gz"

        with tarfile.open(input_tarfile, read_param) as tar_in:
            for encoded_image in tar_in:
                if encoded_image.isfile():
                    try:
                        image_name = encoded_image.name
                        img_data = Image.open(io.BytesIO(tar_in.extractfile(encoded_image).read()))
                        yield img_data, image_name
                    except Exception as e:
                        print("An error occured: ", e)


    def yield_snippet_and_name(self, tarfile_name: str, image_name: str, image: Image.Image):
        for field_name, box_coordinates in self.map_coordinates_to_images[tarfile_name][image_name]:
            yield f"{os.path.splitext(tarfile_name)[0]}_{os.path.splitext(image_name)[0]}_{field_name}.jpg", image.crop(box_coordinates)
