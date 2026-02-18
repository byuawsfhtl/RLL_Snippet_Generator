from typing import Tuple
import pandas as pd

REQUIRED_COLUMNS = set([
    "image_name",
    "snip_name",
    "x1",
    "y1",
    "x2",
    "y2",
    "x3",
    "y3",
    "x4",
    "y4",
])


class CustomException(Exception):
    """A custom exception class. Used to identify error with our scripts."""

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


def convert_df_to_map(df: pd.DataFrame):
    """
    Take the relevant contents from the dataframe and put in in dictionary format to
    facilitate the lookup time of getting the coordinate information for a field on an image we encounter through iteration.

    Args:
        df: A DataFrame object that contains at least the following information: reel_filename, image_name, snip_name, x1, y1, ... x4, y4.
    """

    _validate_dataframe(df)

    # Convert dataframe to dictionary format:
    # The dictionary will be in the format:
    #   {image_name: [(field_name, (x1, y1, x2, y2)), ...], ...}
    image_to_coord_dict = {}
    for row in df.itertuples():
        try:
            image_name, snip_name, box_coordinates = (
                _parse_dataframe_row(row)
            )

            _build_dict(
                image_to_coord_dict,
                image_name,
                snip_name,
                box_coordinates,
            )

        except CustomException as e:
            print("Unexpected error: ", e)

    return image_to_coord_dict


def _validate_dataframe(df: pd.DataFrame):
    """
    Purpose: Validates the structure of the input DataFrame,
    Args:
        df: A pandas DataFrame object.

    Returns:
        Throw exception if df is invalid.
        Invalid: df is empty, df is missing columns, df has nan or None values in any of the required columns.
    """

    # Check if dataframe is empty
    if len(df.columns) == 0:
        raise CustomException(
            f"Dataframe is empty; requires the following columns: {REQUIRED_COLUMNS}"
        )

    # Check if dataframe has the necessary columns to work with Snippet Generator
    df_cols = set(df.columns)
    for column_name in df_cols:
        if column_name not in REQUIRED_COLUMNS:
            raise CustomException(
            f"Dataframe doesn't have the necessary columns to work with Snippet Generator. Missing column: {column_name}"
            )

    # Check for NaN or None values in the dataframe for the required columns
    for column in REQUIRED_COLUMNS:
        if (df[column].isnull() | df[column].isna()).any():
            raise CustomException(
                f"Dataframe has NaN or None values in column: {column}\n Please remove these values."
            )
    
    # Check if cornerpoints are valid numbers (should be a positive integer or zero)
    cornerpoint_columns = ["x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"]
    for column in cornerpoint_columns:
        # Try to cast all values in the column to numeric, then check for strings
        series = pd.to_numeric(df[column], errors='coerce')
        if (series.isnull().any()):
            raise CustomException(
                f"Dataframe has non-numeric values in column: {column}\n All cornerpoint values should be positive integers or zero."
            )
        is_int = (series >= 0).all() and (series % 1 == 0).all()
        if not is_int:
            raise CustomException(
                f"Dataframe has non-integer or negative values in column: {column}\n All cornerpoint values should be positive integers or zero."
            )


def _parse_dataframe_row(row: pd.Series):
    """
    This function helps the convert_df_to_map function by checking for needed information in a validated dataframe's row,
    then returns valid information.

    Args:
        row: A pandas series object that represents a row from the pandas dataframe.
    """

    image_name, snip_name = (
        row.image_name,
        row.snip_name,
    )
    box_coordinates = _get_box_coordinates(row)
    return image_name, snip_name, box_coordinates


def _get_box_coordinates(row: pd.Series):
    """
    This is a helper function for the _parse_dataframe_row function. It returns the box coordinates for a field on an image.

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


def _build_dict(
    dict_of_image_to_field_to_coordinates: dict,
    image_name: str,
    snip_name: str,
    box_coordinates: Tuple
):
    """
    This is a helper function for the convert_df_to_map function. It checks to see if an image_name exists in our dictionary. If not, it adds it.

    Args:
        dict_of_image_to_field_to_coordinates: This is the dictionary that maps images to a list of tuples, where each tuple contains a field name and the coordinates for that field on the image. This is the dictionary that will be used to facilitate lookup time when we are iterating through the images in the reels.
        reel_filename: This is the filename of the file
        image_name: This is the filename of the image.
        snip_name: This is the name of the field on the image that will be snipped, or its coordinats
        box_coordinates: This is a tuple that contains the coordinates to crop a snippets from an image.
    """
    if image_name not in dict_of_image_to_field_to_coordinates:
        dict_of_image_to_field_to_coordinates[image_name] = []

    dict_of_image_to_field_to_coordinates[image_name].append(
        (snip_name, box_coordinates)
    )