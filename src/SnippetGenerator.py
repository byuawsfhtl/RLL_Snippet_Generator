"""
This script takes an image and image directory files from a tarfile
and a directory of json files that came from those images.
It links the json to the images via a map.
It then opens each image and creates snippets of the image based on the corner points in the json file.
"""

import tarfile as tf
import json
import numpy as np
import cv2
from PIL import Image
from typing import Tuple


class SnippetGenerator:
    """
    This class generates image snippets from a tar file containing images
    and a tar file containing json files with corner points.
    """

    # Constructor for this class

    def __init__(self, tar1, tar2):
        """
        Initializes the snippet_generator class with the paths to the tar files containing images and json files.

        Args:
        tar1 (str): Path to the tar file containing images.
        tar2 (str): Path to the tar file containing json files.
        """
        self.image_tar_path = tar1
        self.json_tar_path = tar2
        self.name_to_json = dict()
        self.image_names = set()

    def image_snippet_generator(
        self,
        image: Image.Image,
        name: str,
        desired_snippets: set = None,
        get_all_snippets: bool = True,
    ) -> Image.Image:
        """
        Generates image snippets from a given image and its corresponding json file.

        Args:
        image: PIL.Image.Image. The image to generate snippets from.
        name: str. The name of the image.
        _desired_snippets_: set. A list of snippets that the user wants. Optional, defaults to none.
        _get_all_snippets_: bool. True if user wants to recieve all snippets. Optional, defaults to true.

        Yields:
        tuple: A tuple containing the cropped image and its name.
        """
        if name in self.name_to_json:
            json_data = self.name_to_json[name]
            tables = json_data["tables"]
            for table in tables:
                columns_and_rows = table["points"]
                for col in range(len(columns_and_rows) - 1):
                    for row in range(len(columns_and_rows[0]) - 1):
                        if not get_all_snippets and (row, col) not in desired_snippets:
                            continue
                        # Only get the fields
                        if "Field" not in table["label"]:
                            continue
                        left_top_corner = columns_and_rows[col][row]
                        right_top_corner = columns_and_rows[col + 1][row]
                        bottom_right_corner = columns_and_rows[col + 1][row + 1]
                        bottom_left_corner = columns_and_rows[col][row + 1]
                        left_side = min(left_top_corner[0], bottom_left_corner[0])
                        upper_side = min(left_top_corner[1], right_top_corner[1])
                        right_side = max(bottom_right_corner[0], right_top_corner[0])
                        lower_side = (
                            max(bottom_right_corner[1], bottom_left_corner[1]) + 3
                        )
                        # Crop the image
                        cropped_image = image.crop(
                            (left_side, upper_side, right_side, lower_side)
                        )
                        # Create a name for the image
                        cropped_image_name = f"{table['label']}_row_{row}_col_{col}.png"
                        # Generate the snippet
                        yield cropped_image, cropped_image_name
        else:
            raise ValueError("Image not found in the json file")

    def image_from_tar_generator(self, image_path: str) -> Tuple[Image.Image, str]:
        """
        Generates images from a tar file containing images.

        Args:
        image_path (str): The path to the tar file containing images.

        Yields:
        tuple: A tuple containing the original image and its name.
        """
        set_of_img_extensions = {"png", "jpg", "jpeg", "jp2", "tif", "tiff"}
        with tf.open(image_path, mode="r") as tar_file:
            # Iterate through each member of the tarfile
            for member in tar_file:
                extension = member.name.split(".")[-1]
                name = member.name.split(".")[0]
                if name in self.image_names:
                    continue
                # If it is an image decode it and create the snippets
                if extension in set_of_img_extensions and len(self.name_to_json) > 0:
                    # Check if the image name is in the json file
                    if name in self.name_to_json:
                        # Extract the image data from the tarfile
                        img_data = np.asarray(
                            bytearray(tar_file.extractfile(member).read()),
                            dtype=np.uint8,
                        )
                        # Decode the image file
                        cv2_image = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
                        if cv2_image is not None:
                            # Create an Image
                            original_image = Image.fromarray(cv2_image)
                            self.image_names.add(name)
                            yield original_image, name
                        else:
                            # Image decoding failed
                            raise ValueError(
                                f"cv2_image {name} is None. Image decoding failed."
                            )
                else:
                    raise ValueError(
                        f"Wrong file type. File was {name}. Please ensure that the tar includes only image files"
                    )

    def extract_json(self, input_path: str) -> None:
        """
        Extracts json files from a tar file and stores them in a dictionary.

        Args:
        input_path (str): The path to the tar file containing json files.
        """
        with tf.open(input_path, mode="r") as tar_file:
            # Iterate through each member of the tarfile
            for member in tar_file:
                name = member.name.split(".")[0]
                # If it is a json file extract it and store it in a dictionary
                if member.isfile() and member.name.endswith(".json"):
                    json_data = tar_file.extractfile(member)
                    dict_with_corner_points = json.load(json_data)
                    self.name_to_json[name] = dict_with_corner_points
                    # print(member)
                else:
                    print(
                        f"Wrong file type. File name was {name}. Please ensure that the tar includes only JSON files"
                    )
