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

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the snippet_generator class with the paths to the tar files containing images and json files.

        Args:
            df: A DataFrame object that should contain at least the following information: reel_filename, image_filename, snip_name, x1, y1, ... x4, y4.
        """

        self.map_coordinates_to_images = (
            DataFrame_to_Dictionary_converter().convert_df_to_map(df)
        )

    def save_snippets_to_directory(
        self, input_tarfiles: list, output_directory: str, batch_size: int = 10000
    ):
        """
        This function will generate snippets for the user and save them out a directory. The directory structure will be output_directory -> reel_name -> image_name -> snippet.

        Args:
            input_tarfiles: The paths to the tarfiles that contains images to be snipped.
            output_directory: This is the path to a directory where many directories will be created, and where snippets will be saved to.
            batch_size: This function saves out images in batches to optimize IO performance. batch_size is given a default value.
        """
        for (
            tarfile_name_no_ext,
            image_filenames_no_ext,
            snippet_filenames,
            snippets,
        ) in self.get_batches_of_snippets(input_tarfiles, batch_size):
            for image_filename_no_ext, snippet_filename, snippet in zip(
                image_filenames_no_ext, snippet_filenames, snippets
            ):
                snippet_directory = os.path.join(
                    output_directory, tarfile_name_no_ext, image_filename_no_ext
                )
                path_to_snippet = os.path.join(snippet_directory, snippet_filename)

                if not os.path.exists(snippet_directory):
                    os.makedirs(snippet_directory)

                snippet.save(path_to_snippet)

    def save_snippets_as_tar(
        self,
        input_tarfiles: list,
        output_directory: str,
        outfile: str,
        batch_size: int = 10000,
    ):
        """
        This function will generate snippets for the user and save them out a tar file. The directory structure within the tarfile will be reel_name -> image_name -> snippet.

        Args:
            input_tarfiles: The paths to the tarfiles that contains images to be snipped.
            output_directory: This is the path to a directory where many directories will be created, and where snippets will be saved to.
            outfile: The name of the output file to save the snippets to. This should be a .tar or .tar.gz file.
            batch_size: This function saves out images in batches to optimize IO performance. batch_size is given a default value.
        """
        if not (outfile.endswith(".tar") or outfile.endswith(".tar.gz")):
            raise CustomException(
                f"Output tarfile in the save_snippets_as_tar function must have the correct file extension. Ie: .tar or .tar.gz. You provided extension: {os.path.splitext(outfile)[-1]}"
            )

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        outfile_path = os.path.join(output_directory, outfile)

        write_param = "w"
        outfile_name_no_ext = os.path.splitext(outfile)[0]

        if outfile.endswith("gz"):
            write_param = "w:gz"
            outfile_name_no_ext = os.path.splitext(outfile_name_no_ext)[0]

        with tarfile.open(outfile_path, write_param) as tar_out:
            for (
                tarfile_name_no_ext,
                image_filenames_no_ext,
                snippet_filenames,
                snippets,
            ) in self.get_batches_of_snippets(input_tarfiles, batch_size):
                for image_filename_no_ext, snippet_filename, snippet in zip(
                    image_filenames_no_ext, snippet_filenames, snippets
                ):
                    try:
                        snippet_byte_arr = io.BytesIO()
                        snippet.save(snippet_byte_arr, format="PNG")
                        snippet_byte_arr.seek(0)

                        tar_path = os.path.join(
                            outfile_name_no_ext,
                            tarfile_name_no_ext,
                            image_filename_no_ext,
                            snippet_filename,
                        )

                        snippet_info = tarfile.TarInfo(name=tar_path)
                        snippet_info.size = len(snippet_byte_arr.getvalue())

                        tar_out.addfile(snippet_info, snippet_byte_arr)
                    except Exception as e:
                        print(snippet_filename)
                        print(e)

    def get_batches_of_snippets(self, input_tarfiles: list, batch_size: int):
        """
        This function yields a batch of snippets from one or more images.

        Args:
            input_tarfiles: The paths to the tarfiles that contains images to be snipped.
            batch_size: The number of snippets we want this function to yield at a given time.
        """

        for input_tarfile in input_tarfiles:
            tarfile_name = os.path.basename(input_tarfile)

            if not (tarfile_name.endswith(".tar") or tarfile_name.endswith(".tar.gz")):
                raise CustomException(
                    f"Input tarfile in the save_snippets_as_tar function must have the correct file extension. Ie: .tar or .tar.gz. You provided extension: {os.path.splitext(tarfile_name)[-1]}"
                )

            tarfile_name_no_ext = os.path.splitext(tarfile_name)[0]

            if tarfile_name.endswith(".tar.gz"):
                tarfile_name_no_ext = os.path.splitext(tarfile_name_no_ext)[0]

            if tarfile_name not in self.map_coordinates_to_images:
                continue
            else:
                snippets, snippet_filenames, image_names_no_ext = [], [], []
                for image_name, image in self.yield_image_and_name(input_tarfile):
                    image_name_no_ext = os.path.splitext(image_name)[0]
                    for snippet_filename, snippet in self.yield_snippet_and_name(
                        tarfile_name, image_name, image
                    ):
                        snippets.append(snippet)
                        snippet_filenames.append(snippet_filename)
                        image_names_no_ext.append(image_name_no_ext)

                        if len(snippets) == batch_size:
                            yield (
                                tarfile_name_no_ext,
                                image_names_no_ext,
                                snippet_filenames,
                                snippets,
                            )
                            snippets, snippet_filenames, image_names_no_ext = [], [], []

                if snippets and snippet_filenames:
                    yield (
                        tarfile_name_no_ext,
                        image_names_no_ext,
                        snippet_filenames,
                        snippets,
                    )

    def yield_image_and_name(self, input_tarfile: str):
        """
        This function open and iterates through the images in the tar file.
        It decodes the image fiels into memory and returns the image data in a PIL.Image object. It also returns the image file_name

        Args:
            input_tarfile: The path to the tarfile that contains images to be snipped.
        """

        read_param = "r"
        if input_tarfile.endswith("gz"):
            read_param = "r:gz"

        input_tarfile_basename = os.path.basename(input_tarfile)

        with tarfile.open(input_tarfile, read_param) as tar_in:
            for encoded_image in tar_in:
                if encoded_image.isfile():
                    try:
                        image_filename = encoded_image.name
                        if (
                            image_filename
                            not in self.map_coordinates_to_images[
                                input_tarfile_basename
                            ]
                        ):
                            continue
                        else:
                            img_data = Image.open(
                                io.BytesIO(tar_in.extractfile(encoded_image).read())
                            )
                            yield image_filename, img_data

                    except Exception as e:
                        print("An error occured: ", e)

    def yield_snippet_and_name(
        self, tarfile_name: str, image_filename: str, image: Image.Image
    ):
        """
        This function returns the snippets for an image and the future filename of the newly created snippet.

        Args:
            tarfile_name: This is the name of the input_tarfile with the file extension.
            image_file_name: This is the name of the image file with the file extension.
            image: This is the PIL.Image that we will snip the snippets from.
        """
        image_filename_no_ext = os.path.splitext(image_filename)[0]
        tarfile_name_no_ext = os.path.splitext(tarfile_name)[0]

        if tarfile_name.endswith("gz"):
            tarfile_name_no_ext = os.path.splitext(tarfile_name_no_ext)[0]

        for field_name, box_coordinates in self.map_coordinates_to_images[tarfile_name][
            image_filename
        ]:
            try:
                self.validate_box_coordinates(box_coordinates)

                yield (
                    f"{tarfile_name_no_ext}_{image_filename_no_ext}_{field_name}.png",
                    image.crop(box_coordinates),
                )
            except Exception as e:
                print("Error occured: ", e)
                continue

    def validate_box_coordinates(self, box_coordinates: tuple):
        if (box_coordinates[2] - box_coordinates[0]) <= 0:
            raise CustomException(
                f"The width of the cropped image must be positive and nonzero. Left and right box coordinates: {box_coordinates[0]}, {box_coordinates[2]}"
            )
        if (box_coordinates[3] - box_coordinates[1]) <= 0:
            raise CustomException(
                f"The height of the cropped image must be positive and nonzero. Top and bottom box coordinates: {box_coordinates[1]}, {box_coordinates[3]}"
            )


class DataFrame_to_Dictionary_converter:
    def convert_df_to_map(self, df: pd.DataFrame):
        """
        When we iterate through tarfiles and extract their images, the ordering of the images may not match the ordering of the images
        in the dataframe that is passed into the class. As such, we take the relevant contents from the dataframe and put in in dictionary format to
        facilitate the lookup time of getting the coordinate information for a field on the image.

        Args:
            df: A DataFrame object that contains at least the following information: reel_filename, image_filename, snip_name, x1, y1, ... x4, y4.
        """

        if not self.check_dataframe_has_valid_columns(df):
            raise CustomException(
                "Dataframe doesn't have the necessary columns to work with Snippet Generator."
            )

        dict_of_reel_image_field_to_coordinates = {}

        for row in df.itertuples():
            try:
                reel_filename, image_filename, snip_name, box_coordinates = (
                    self.get_info_from_dataframe_row(row)
                )

                if reel_filename in dict_of_reel_image_field_to_coordinates:
                    self.check_if_image_filename_in_dict(
                        dict_of_reel_image_field_to_coordinates,
                        reel_filename,
                        image_filename,
                        snip_name,
                        box_coordinates,
                    )
                else:
                    dict_of_reel_image_field_to_coordinates[reel_filename] = {}
                    self.check_if_image_filename_in_dict(
                        dict_of_reel_image_field_to_coordinates,
                        reel_filename,
                        image_filename,
                        snip_name,
                        box_coordinates,
                    )
            except CustomException as e:
                print("Found error: ", e)

        return dict_of_reel_image_field_to_coordinates

    def check_dataframe_has_valid_columns(self, df: pd.DataFrame):
        """
        This function ensures that the dataframe passed into the snippet generator has
        the minimum columns necesarry to generate snippets.

        Args:
            df: A DataFrame object that should contain at least the following information: reel_filename, image_filename, snip_name, x1, y1, ... x4, y4.
        """

        if len(df.columns) == 0:
            return False

        needed_columns = [
            "reel_filename",
            "image_filename",
            "snip_name",
            "x1",
            "y1",
            "x2",
            "y2",
            "x3",
            "y3",
            "x4",
            "y4",
        ]
        set_of_column_names_from_df = set(df.columns)

        for column_name in needed_columns:
            if column_name not in set_of_column_names_from_df:
                return False

        return True

    def get_info_from_dataframe_row(self, row: pd.Series):
        """
        This function helps the convert_df_to_map function by checking that the relvant information is found in a dataframe row, it then returns that information.

        Args:
            row: A pandas series object that represents a row from the pandas dataframe.
        """
        if any(self.check_for_errors(x) for x in row):
            raise CustomException(
                f"None or Nan values found in dataframe at row: {row.reel_filename}, {row.image_filename}, {row.snip_name}"
            )
        else:
            reel_filename, image_filename, snip_name = (
                row.reel_filename,
                row.image_filename,
                row.snip_name,
            )
            box_coordinates = self.get_box_coordinates(row)
            return reel_filename, image_filename, snip_name, box_coordinates

    def check_for_errors(self, x: object):
        """
        This is a helper function for the get_info_from_dataframe_row function. It checks if a value is None or Nan.

        Args:
            x: This is a variable that comes from a row in a dataframe.
        """
        if isinstance(x, float):
            if math.isnan(x):
                return True
            else:
                return False
        elif x is None:
            return True
        else:
            return False

    def get_box_coordinates(self, row: pd.Series):
        """
        This is a helper function for the get_info_from_dataframe_row function. It returns the box coordinates for a field on an image.

        Args:
            row: A pandas series object that represents a row from the pandas dataframe.
        """
        x_coordinates = [row.x1, row.x2, row.x3, row.x4]
        y_coordinates = [row.y1, row.y2, row.y3, row.y4]

        left, upper, right, lower = (
            min(x_coordinates),
            min(y_coordinates),
            max(x_coordinates),
            max(y_coordinates),
        )

        return (left, upper, right, lower)

    def check_if_image_filename_in_dict(
        self,
        dict_of_reel_image_field_to_coordinates: dict,
        reel_filename: str,
        image_filename: str,
        snip_name: str,
        box_coordinates: Tuple,
    ):
        """
        This is a helper function for the convert_df_to_map function. It checks to see if an image_filename exists in our dictionary. If not, it adds it.

        Args:
            dict_of_reel_image_field_to_coordinates: This is the dictionary that tracks reel to image, image to field and coordinates.
            reel_filename: This is the filename of the reel. Ie: 14.tar
            image_filename: This is the filename of the image. Ie: 987.png
            snip_name: This is the name of the field on the image that will be snipped. Ie: person_name
            box_coordinates: This is a tuple that contains the coordinates to crop a snippets from an image.
        """
        if image_filename in dict_of_reel_image_field_to_coordinates[reel_filename]:
            self.add_field_and_coordinates(
                dict_of_reel_image_field_to_coordinates,
                reel_filename,
                image_filename,
                snip_name,
                box_coordinates,
            )
        else:
            dict_of_reel_image_field_to_coordinates[reel_filename][image_filename] = []
            self.add_field_and_coordinates(
                dict_of_reel_image_field_to_coordinates,
                reel_filename,
                image_filename,
                snip_name,
                box_coordinates,
            )

    def add_field_and_coordinates(
        self,
        dict_of_reel_image_field_to_coordinates: dict,
        reel_filename: str,
        image_filename: str,
        snip_name: str,
        box_coordinates: Tuple,
    ):
        """
        This is a helper function for the check_if_image_filename_in_dict function. See that function for argument definitions.
        """
        dict_of_reel_image_field_to_coordinates[reel_filename][image_filename].append(
            (snip_name, box_coordinates)
        )
