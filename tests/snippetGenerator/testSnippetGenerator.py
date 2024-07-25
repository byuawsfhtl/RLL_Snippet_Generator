import unittest
import os
from PIL import Image, ImageChops
import pandas as pd
import math
import shutil
import subprocess
import sys

current = os.path.dirname(os.path.realpath(__file__))
testFolder = os.path.dirname(current)
root = os.path.dirname(testFolder)
sys.path.append(os.path.join(root, "src"))

from SnippetGenerator import (  # noqa: E402
    SnippetGenerator,  # noqa: E402
    DataFrame_to_Dictionary_converter,  # noqa: E402
    CustomException,  # noqa: E402
)  # noqa: E402


class SnippetGenerator_Tests(unittest.TestCase):
    """
    This class tests all the functions in the SnippetGenerator class. The functions in this class that are named test_'corresponding snippet generator function' test a function from the
    SnippetGenerator class. All other functions are helper functions to the test functions.
    """

    def setUp(self):
        self.df_column_names = [
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
        self.image_tar_path = os.path.join("tests", "resources", "iowa_image.tar")
        self.image_tar_path_compressed = os.path.join(
            "tests", "resources", "iowa_image_gz.tar.gz"
        )
        self.image_zip_path = os.path.join("tests", "resources", "iowa_image.zip")
        self.iowa_tsv_path = os.path.join("tests", "resources", "iowa.tsv")
        self.snippet_tar_path = os.path.join("tests", "resources", "snippet.tar")
        self.df = pd.read_csv(self.iowa_tsv_path, sep="\t")
        self.snippet_generator = SnippetGenerator(self.df)
        self.dataframe_converter = DataFrame_to_Dictionary_converter()

    def test_custom_exception_class(self):
        error_message = "error"
        expected_error_message = "CustomException: " + error_message

        custom_exception = CustomException(error_message)
        actual_error_message = custom_exception.__str__()

        assert actual_error_message == expected_error_message

    def test_check_dataframe_has_valid_columns(self):
        # positive case
        df_1 = pd.DataFrame(columns=self.df_column_names)
        df_2 = pd.DataFrame(
            columns=[
                "reel_filename",
                "other_field_1",
                "image_filename",
                "snip_name",
                "x1",
                "y1",
                "x2",
                "y2",
                "x3",
                "other_filed_2",
                "y3",
                "x4",
                "y4",
            ]
        )

        assert self.dataframe_converter.check_dataframe_has_valid_columns(df_1)
        assert self.dataframe_converter.check_dataframe_has_valid_columns(df_2)

        # negative case
        df_1 = df_1.drop(columns=["reel_filename"])
        df_3 = pd.DataFrame()

        assert not self.dataframe_converter.check_dataframe_has_valid_columns(df_1)
        assert not self.dataframe_converter.check_dataframe_has_valid_columns(df_3)

    def test_check_for_errors(self):
        # Test a None value
        assert self.dataframe_converter.check_for_errors(None)

        # Test a Nan value
        assert self.dataframe_converter.check_for_errors(math.nan)

        # Test regular values
        assert not self.dataframe_converter.check_for_errors(3.0)
        assert not self.dataframe_converter.check_for_errors(3)
        assert not self.dataframe_converter.check_for_errors("3")

    def test_get_box_coordinates(self):
        row_1 = [1, 1, 1, 2, 2, 1, 2, 2]
        row_2 = [9, 4, 2, 7, 3, 7, 1, 5]

        df = pd.DataFrame(
            data=[row_1, row_2],
            columns=["x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"],
        )

        series_1 = df.iloc[0]
        series_2 = df.iloc[1]

        l1, u1, r1, d1 = self.dataframe_converter.get_box_coordinates(series_1)
        l2, u2, r2, d2 = self.dataframe_converter.get_box_coordinates(series_2)

        assert l1 == row_1[0] and u1 == row_1[1] and r1 == row_1[4] and d1 == row_1[7]
        assert l2 == row_2[6] and u2 == row_2[1] and r2 == row_2[0] and d2 == row_2[3]

    def test_get_info_from_dataframe_row(self):
        # postive case
        info = ["reel_1.tar", "image_1.jpg", "person_name", 1, 1, 1, 2, 2, 1, 2, 2]
        df = pd.DataFrame(data=[info], columns=self.df_column_names)
        row = df.iloc[0]
        reel_filename, image_filename, snip_name, box_coordinates = (
            self.dataframe_converter.get_info_from_dataframe_row(row)
        )
        assert (
            box_coordinates[0] == row[3]
            and box_coordinates[1] == row[4]
            and box_coordinates[2] == row[7]
            and box_coordinates[3] == row[10]
        )
        assert (
            reel_filename == row[0] and image_filename == row[1] and snip_name == row[2]
        )

        # negative case
        try:
            info = ["reel_1.tar", None, "person_name", 1, 1, 1, 2, math.nan, 1, 2, 2]
            df = pd.DataFrame(data=[info], columns=self.df_column_names)
            row = df.iloc[0]
            _ = self.dataframe_converter.get_info_from_dataframe_row(row)
        except Exception as e:
            expected_exception_messsage = "CustomException: None or Nan values found in dataframe at row: reel_1.tar, None, person_name"
            exception_message = e.__str__()
            assert exception_message == expected_exception_messsage

    def test_add_field_and_coordinates_and_check_if_image_filename_in_dict(self):
        # set up
        reel_filename, image_filename = "reel_1.tar", "image_1.jpg"
        snip_name, box_coordinates = "person_name", (1, 1, 2, 2)

        # case 1
        temp_dict = {reel_filename: {image_filename: []}}
        self.dataframe_converter.check_if_image_filename_in_dict(
            temp_dict, reel_filename, image_filename, snip_name, box_coordinates
        )

        assert temp_dict[reel_filename][image_filename][0][0] == snip_name
        assert temp_dict[reel_filename][image_filename][0][1] == box_coordinates

        # case 2
        temp_dict = {reel_filename: {}}
        self.dataframe_converter.check_if_image_filename_in_dict(
            temp_dict, reel_filename, image_filename, snip_name, box_coordinates
        )

        assert temp_dict[reel_filename][image_filename][0][0] == snip_name
        assert temp_dict[reel_filename][image_filename][0][1] == box_coordinates

    def test_convert_df_to_map(self):
        df = pd.read_csv(self.iowa_tsv_path, sep="\t")

        reel_filename = df.iloc[1][0]
        assert reel_filename in self.snippet_generator.map_coordinates_to_images

        all_image_names_in_dict = True

        for image_filename in df["image_filename"].unique():
            if (
                image_filename
                not in self.snippet_generator.map_coordinates_to_images[reel_filename]
            ):
                all_image_names_in_dict = False

        assert all_image_names_in_dict

        try:
            df = pd.DataFrame(
                [["reel_1.tar", "image_1.jpg", "person_name", 1, 1, 1, 2, 2, 1, 2]],
                columns=[
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
                ],
            )
            self.dataframe_converter.convert_df_to_map(df)
        except Exception as e:
            assert (
                e.__str__()
                == "CustomException: Dataframe doesn't have the necessary columns to work with Snippet Generator."
            )

    def test_yield_image_and_name(self):
        test_image = Image.open(os.path.join("tests", "resources", "iowa.jpg"))

        for tar_image_name, image in self.snippet_generator.yield_image_and_name(
            self.image_tar_path
        ):
            assert tar_image_name == "iowa"

            if test_image.size == image.size and test_image.mode == image.mode:
                # Compute the difference between the images, returns an image whose pixel values are abs(image_1.pixel_at_xy - image_2.pixel_at_xy)
                diff = ImageChops.difference(test_image, image)

                # Find the bounding box of the non-zero regions of the image, if there is no region, return None
                assert diff.getbbox() is None
            else:
                assert False

    def test_yield_snippet_and_field(self):
        test_snippet = Image.open(
            os.path.join("tests", "resources", "iowa_image_iowa_Card_No.png")
        )

        for image_name, image in self.snippet_generator.yield_image_and_name(
            self.image_tar_path
        ):
            for field, snippet in self.snippet_generator.yield_snippet_and_field(
                os.path.splitext(os.path.basename(self.image_tar_path))[0],
                image_name,
                image,
            ):
                assert field == "Card_No"

                if (
                    test_snippet.size == snippet.size
                    and test_snippet.mode == snippet.mode
                ):
                    # Compute the difference between the images, returns an image whose pixel values are abs(image_1.pixel_at_xy - image_2.pixel_at_xy)
                    diff = ImageChops.difference(test_snippet, snippet)

                    # Find the bounding box of the non-zero regions of the image, if there is no region, return None
                    assert diff.getbbox() is None
                    break
                else:
                    assert False

        self.snippet_generator.map_coordinates_to_images["snippet"] = {}
        # (snip_name, box_coordinates) (left, upper, right, lower)
        self.snippet_generator.map_coordinates_to_images["snippet"][
            "iowa_image_iowa_Card_No"
        ] = [
            ("Test_snip_1", (0, 0, 0, 0)),
            ("Test_snip_2", (3, 3, 2, 5)),
            ("Test_snip_3", (3, 3, 5, 2)),
            ("Test_snip_4", (3, 3, 1, 1)),
        ]

        nothing_was_yielded = True

        for image_name, image in self.snippet_generator.yield_image_and_name(
            self.snippet_tar_path
        ):
            for snip_name, snippet in self.snippet_generator.yield_snippet_and_field(
                os.path.splitext(os.path.basename(self.snippet_tar_path))[0],
                image_name,
                image,
            ):
                nothing_was_yielded = False

        assert nothing_was_yielded

        self.snippet_generator.map_coordinates_to_images.pop("snippet")

    def test_get_batches_of_snippets(self):
        images_per_batch = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 1]

        batch_sizes_are_equal = True

        for expected_batch_size, (_, _, snippet_names, _) in zip(
            images_per_batch,
            self.snippet_generator.get_batches_of_snippets([self.image_tar_path], 10),
        ):
            if expected_batch_size != len(snippet_names):
                batch_sizes_are_equal = False

        assert batch_sizes_are_equal

        try:
            for _, _, _, _ in self.snippet_generator.get_batches_of_snippets(
                ["path/to/not_a_real_tarfile.tar", self.image_zip_path], 10
            ):
                pass
        except Exception as e:
            assert (
                e.__str__()
                == "CustomException: Input tarfile in the save_snippets_as_tar function must have the correct file extension. Ie: .tar or .tar.gz. You provided extension: .zip"
            )

    def test_save_snippets_to_directory(self):
        out_dir = os.path.join("tests", "output")

        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)
            os.makedirs(out_dir)
        else:
            os.makedirs(out_dir)

        self.snippet_generator.save_snippets_to_directory(
            [self.image_tar_path], out_dir
        )

        snippet_paths_are_equal = self.compare_actual_paths_to_expected_paths(
            out_dir, None
        )

        assert snippet_paths_are_equal

        shutil.rmtree(out_dir)

    def test_save_snippets_as_tar(self):
        for archive_path in [self.image_tar_path, self.image_tar_path_compressed]:
            for ext in [".tar.gz", ".tar"]:
                out_dir = os.path.join("tests", "output")

                if os.path.exists(out_dir):
                    shutil.rmtree(out_dir)

                tarfile_in_name = os.path.splitext(os.path.basename(archive_path))[0]
                if archive_path.endswith("gz"):
                    tarfile_in_name = os.path.splitext(tarfile_in_name)[0]

                tarfile_out_filename_no_ext = tarfile_in_name + "_snippets"
                tarfile_out_filename = tarfile_out_filename_no_ext + ext

                self.snippet_generator.save_snippets_as_tar(
                    [archive_path], out_dir, tarfile_out_filename
                )

                assert tarfile_out_filename in os.listdir(out_dir)

                try:
                    subprocess.run(
                        [
                            "tar",
                            "-xf",
                            os.path.join(out_dir, tarfile_out_filename),
                            "-C",
                            out_dir,
                        ]
                    )
                    print("Extracted tarfile")
                except subprocess.CalledProcessError as e:
                    print("Extraction failed: ")
                    print(e)

                os.remove(os.path.join(out_dir, tarfile_out_filename))

                snippet_paths_are_equal = self.compare_actual_paths_to_expected_paths(
                    out_dir, tarfile_out_filename_no_ext
                )

                assert snippet_paths_are_equal

                shutil.rmtree(out_dir)

        try:
            self.snippet_generator.save_snippets_as_tar(
                [self.image_tar_path], None, "out.zip"
            )

        except Exception as e:
            assert (
                e.__str__()
                == "CustomException: Output tarfile in the save_snippets_as_tar function must have the correct file extension. Ie: .tar or .tar.gz. You provided extension: .zip"
            )

    def compare_actual_paths_to_expected_paths(
        self, out_dir: str, tarfile_out_filename_no_ext: str
    ):
        set_of_snippet_paths = set()
        if tarfile_out_filename_no_ext:
            out_dir = os.path.join(out_dir, tarfile_out_filename_no_ext)

        df = pd.read_csv(self.iowa_tsv_path, sep="\t")

        for row in df.itertuples():
            tarfile_name_no_ext = os.path.splitext(row.reel_filename)[0]
            image_name_no_ext = os.path.splitext(row.image_filename)[0]

            snippet_file = (
                f"{tarfile_name_no_ext}_{image_name_no_ext}_{row.snip_name}.png"
            )
            set_of_snippet_paths.add(
                os.path.join(
                    out_dir, tarfile_name_no_ext, image_name_no_ext, snippet_file
                )
            )

        list_of_snippet_paths = []

        self.recursive_helper(out_dir, list_of_snippet_paths)

        snippet_paths_are_equal = True

        for snippet_path in list_of_snippet_paths:
            if snippet_path not in set_of_snippet_paths:
                snippet_paths_are_equal = False

        return snippet_paths_are_equal

    def recursive_helper(self, path, list_of_filepaths):
        if os.path.isdir(path):
            for object in os.listdir(path):
                new_path = os.path.join(path, object)
                self.recursive_helper(new_path, list_of_filepaths)
        else:
            list_of_filepaths.append(path)


if __name__ == "__main__":
    unittest.main()
