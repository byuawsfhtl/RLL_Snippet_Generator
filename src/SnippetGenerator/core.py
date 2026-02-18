import tarfile
import io
import os

import pandas as pd
from PIL import Image

from . import utils

class SnippetGenerator:
    """
    This class generates image snippets from a tar file containing images
    and a pandas dataframe that contains coordinate information for the snippets.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Assign paths to the tar files containing images and json files.

        Args:
            df: A DataFrame object that should contain at least the following information:
                reel_name, image_name, snip_name, x1, y1, ... x4, y4.
            cps = cornerpoints
        """

        self.images_to_cps_map = (
            utils.convert_df_to_map(df)
        )


    def save_snippets_to_directory_from_tarfiles(
        self,
        input_tarfiles: list,
        output_directory: str,
        batch_size: int = 10000,
        buffer: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        """
        This function will generate snippets for the user and save them out a directory.
        The directory structure will be output_directory -> reel_name -> image_name -> snippet.

        Args:
            input_tarfiles: The paths to the tarfiles that contains images to be snipped.
            output_directory: This is the path to a directory where many directories will be created,
                and where snippets will be saved to.
            batch_size: This function saves out images in batches to optimize IO performance.
                batch_size is given a default value.
            buffer: This is a tuple that contains the buffer values for the snippet.
                The buffer values are [left, upper, right, lower].
                The buffer values are used to expand the snippet beyond the original coordinates.
        """
        for (
            tarfile_name_no_ext,
            image_names_no_ext,
            fields,
            snippets,
        ) in self._get_batches_of_snippets_from_tarfiles(
            input_tarfiles, batch_size, buffer
        ):
            for image_name_no_ext, field, snippet in zip(
                image_names_no_ext, fields, snippets
            ):
                snippet_directory = os.path.join(
                    output_directory, tarfile_name_no_ext, image_name_no_ext
                )
                snippet_filename = f"{image_name_no_ext}_{field}.png"
                path_to_snippet = os.path.join(snippet_directory, snippet_filename)

                if not os.path.exists(snippet_directory):
                    os.makedirs(snippet_directory)

                snippet.save(path_to_snippet)

    def save_snippets_as_tar_from_tarfiles(
        self,
        input_tarfiles: list,
        output_directory: str,
        outfile: str,
        batch_size: int = 10000,
        buffer: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        """
        This function will generate snippets for the user and save them out a tar file. The directory structure within the tarfile will be reel_name -> image_name -> snippet.

        Args:
            input_tarfiles: The paths to the tarfiles that contains images to be snipped.
            output_directory: This is the path to a directory where many directories will be created, and where snippets will be saved to.
            outfile: The name of the output file to save the snippets to. This should be a .tar or .tar.gz file.
            batch_size: This function saves out images in batches to optimize IO performance. batch_size is given a default value.
            buffer: This is a tuple that contains the buffer values for the snippet. The buffer values are [left, upper, right, lower]. The buffer values are used to expand the snippet beyond the original coordinates.
        """
        if not (outfile.endswith(".tar") or outfile.endswith(".tar.gz")):
            raise utils.CustomException(
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
                image_names_no_ext,
                fields,
                snippets,
            ) in self._get_batches_of_snippets_from_tarfiles(
                input_tarfiles, batch_size, buffer
            ):
                for image_name_no_ext, field, snippet in zip(
                    image_names_no_ext, fields, snippets
                ):
                    try:
                        snippet_byte_arr = io.BytesIO()
                        snippet.save(snippet_byte_arr, format="PNG")
                        snippet_byte_arr.seek(0)

                        snippet_filename = f"{image_name_no_ext}_{field}.png"
                        tar_path = os.path.join(
                            outfile_name_no_ext,
                            tarfile_name_no_ext,
                            image_name_no_ext,
                            snippet_filename,
                        )

                        snippet_info = tarfile.TarInfo(name=tar_path)
                        snippet_info.size = len(snippet_byte_arr.getvalue())

                        tar_out.addfile(snippet_info, snippet_byte_arr)
                    except Exception as e:
                        print(snippet_filename)
                        print(e)

    def save_snippets_to_directory_from_image_paths(
        self,
        image_paths: list,
        output_directory: str,
        batch_size: int = 10000,
        buffer: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        for (
            image_names_no_ext,
            fields,
            snippets,
        ) in self.get_batches_of_snippets_from_image_paths(
            image_paths, batch_size, buffer
        ):
            for image_name_no_ext, field, snippet in zip(
                image_names_no_ext, fields, snippets
            ):
                snippet_directory = os.path.join(output_directory, image_name_no_ext)
                snippet_filename = f"{image_name_no_ext}_{field}.png"
                path_to_snippet = os.path.join(snippet_directory, snippet_filename)

                if not os.path.exists(snippet_directory):
                    os.makedirs(snippet_directory)

                snippet.save(path_to_snippet)


    def save_snippets_as_tar_from_image_paths(
        self,
        image_paths: list,
        output_directory: str,
        outfile: str,
        batch_size: int = 10000,
        buffer: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        if not (outfile.endswith(".tar") or outfile.endswith(".tar.gz")):
            raise utils.CustomException(
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
                image_names_no_ext,
                fields,
                snippets,
            ) in self.get_batches_of_snippets_from_image_paths(
                image_paths, batch_size, buffer
            ):
                for image_name_no_ext, field, snippet in zip(
                    image_names_no_ext, fields, snippets
                ):
                    try:
                        snippet_byte_arr = io.BytesIO()
                        snippet.save(snippet_byte_arr, format="PNG")
                        snippet_byte_arr.seek(0)

                        snippet_filename = f"{image_name_no_ext}_{field}.png"
                        tar_path = os.path.join(
                            outfile_name_no_ext,
                            image_name_no_ext,
                            snippet_filename,
                        )

                        snippet_info = tarfile.TarInfo(name=tar_path)
                        snippet_info.size = len(snippet_byte_arr.getvalue())

                        tar_out.addfile(snippet_info, snippet_byte_arr)
                    except Exception as e:
                        print(snippet_filename)
                        print(e)

    def _get_batches_of_snippets_from_tarfiles(
        self,
        input_tarfiles: list,
        batch_size: int,
        buffer: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        """
        This function yields a batch of snippets from one or more images.

        Args:
            input_tarfiles: The paths to the tarfiles that contains images to be snipped.
            batch_size: The number of snippets we want this function to yield at a given time.
            buffer: This is a tuple that contains the buffer values for the snippet.
                The buffer values are [left, upper, right, lower].
                The buffer values are used to expand the snippet beyond the original coordinates.
        """

        for input_tarfile in input_tarfiles:
            # Validate tarfile name and path
            tarfile_name = os.path.basename(input_tarfile)

            if not (tarfile_name.endswith(".tar") or tarfile_name.endswith(".tar.gz")):
                raise utils.CustomException(
                    f"Input tarfile in the _get_batches_of_snippets_from_tarfiles function must have the correct file extension: .tar or .tar.gz. You provided extension: {os.path.splitext(tarfile_name)[-1]} for file: {input_tarfile}"
                )
            if not os.path.exists(input_tarfile):
                raise utils.CustomException(
                    f"The path to this tarfile doesn't exist. {input_tarfile}"
                )

            tarfile_name_no_ext = os.path.splitext(tarfile_name)[0]

            if tarfile_name.endswith(".tar.gz"):
                tarfile_name_no_ext = os.path.splitext(tarfile_name_no_ext)[0]

            snippets, fields, image_names = [], [], []
            for image_name, image in self._yield_image_and_name_from_tarfile(
                input_tarfile
            ):
                for field, snippet in self._yield_snippet_and_field(
                    image_name, image, buffer
                ):
                    snippets.append(snippet)
                    fields.append(field)
                    image_names.append(image_name)

                    if len(snippets) == batch_size:
                        yield (
                            tarfile_name_no_ext,
                            image_names,
                            fields,
                            snippets,
                        )
                        snippets, fields, image_names = [], [], []

            if snippets and fields:
                yield (
                    tarfile_name_no_ext,
                    image_names,
                    fields,
                    snippets,
                )

    def get_batches_of_snippets_from_image_paths(
        self,
        image_paths: list,
        batch_size: int,
        buffer: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        """
        This function yields a batch of snippets from one or more images.

        Args:
            image_paths: The paths to the images that contains
            batch_size: The number of snippets we want this function to yield at a given time.
            buffer: This is a tuple that contains the buffer values for the snippet. The buffer values are [left, upper, right, lower]. The buffer values are used to expand the snippet beyond the original coordinates.
        """
        image_names_no_ext, fields, snippets = [], [], []

        for image_path in image_paths:

            # The original code: Check only if image name is in the map,
            # But since the paths are stored in the map, just check for that:
            # image_name = os.path.splitext(os.path.basename(image_path))[0]

            image_name = image_path

            if image_path not in self.images_to_cps_map:
                continue

            try:
                image = Image.open(image_path)
                for field, snippet in self._yield_snippet_and_field(
                    image_name, image, buffer
                ):
                    image_names_no_ext.append(image_name)
                    fields.append(field)
                    snippets.append(snippet)

                    if len(snippets) == batch_size:
                        yield image_names_no_ext, fields, snippets
                        image_names_no_ext, fields, snippets = [], [], []
            except Exception as e:
                print(e)

        if snippets and fields:
            yield (
                image_names_no_ext,
                fields,
                snippets,
            )

    def _yield_image_and_name_from_tarfile(self, input_tarfile: str):
        """
        This function open and iterates through the images in the tar file.
        It decodes the image files into memory and returns the image data in a PIL.Image object.
        It also returns the image file_name

        Args:
            input_tarfile: The path to the tarfile that contains images to be snipped.
        """

        read_param = "r"
        input_reel_name = os.path.splitext(os.path.basename(input_tarfile))[0]

        if input_tarfile.endswith("gz"):
            read_param = "r:gz"
            input_reel_name = os.path.splitext(input_reel_name)[0]

        with tarfile.open(input_tarfile, read_param) as tar_in:
            for encoded_image in tar_in:
                if encoded_image.isfile():
                    try:
                        image_name = encoded_image.name
                        image_name = os.path.splitext(os.path.basename(image_name))[0]
                        if image_name not in self.images_to_cps_map:
                            continue
                        else:
                            img_data = Image.open(
                                io.BytesIO(tar_in.extractfile(encoded_image).read())
                            )
                            yield image_name, img_data

                    except Exception as e:
                        print("An error occured: ", e)

    def _yield_snippet_and_field(
        self,
        image_name: str,
        image: Image.Image,
        buffer: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        """
        This function returns the snippets for an image and the future filename of the newly created snippet.

        Args:
            image_name: The name of the image that the snippet is being generated from.
            image: The image object that the snippet is being generated from.
            buffer: This is a tuple that contains the buffer values for the snippet. The buffer values are [left, upper, right, lower]. The buffer values are used to expand the snippet beyond the original coordinates.
        """
        for field_name, box_coordinates in self.images_to_cps_map[image_name]:
            box_coordinates = self._expand_box_with_buffer(buffer, box_coordinates)

            try:
                self._validate_box_coordinates(box_coordinates)

                yield (
                    field_name,
                    image.crop(box_coordinates),
                )
            except Exception as e:
                print("Error occured: ", e)
                continue

    def _expand_box_with_buffer(
        self,
        buffer: tuple[int, int, int, int],
        box_coordinates: tuple[int, int, int, int],
    ):
        """
        This function expands the box coordinates by the buffer values.

        Args:
            buffer: This is a list that contains the buffer values for the snippet. The buffer values are [left, upper, right, lower]. The buffer values are used to expand the snippet beyond the original coordinates.

        """
        left, upper, right, lower = box_coordinates
        left = left - buffer[0]
        upper = upper - buffer[1]
        right = right + buffer[2]
        lower = lower + buffer[3]
        box_coordinates = (left, upper, right, lower)
        return box_coordinates


    def _validate_box_coordinates(self, box_coordinates: tuple):
        if (box_coordinates[2] - box_coordinates[0]) <= 0:
            raise utils.CustomException(
                f"The width of the cropped image must be positive and nonzero. Left and right box coordinates: {box_coordinates[0]}, {box_coordinates[2]}"
            )
        if (box_coordinates[3] - box_coordinates[1]) <= 0:
            raise utils.CustomException(
                f"The height of the cropped image must be positive and nonzero. Top and bottom box coordinates: {box_coordinates[1]}, {box_coordinates[3]}"
            )


