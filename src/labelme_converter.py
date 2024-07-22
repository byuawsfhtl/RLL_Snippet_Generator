import os
import sys
import json
import argparse


def read_in_shapes(lm_path):
    # The main part of a LabelMe file is its 'shapes' list. This function reads in the JSON file and returns that list.
    try:
        with open(lm_path, 'r') as file:
            labelme = json.load(file)
            return labelme['shapes']
    except Exception as e:
        print(f'Error while processing LabelMe file: {e}')


def convert_labelme_to_snippet_generator_format(lm_path, out_dir, reel_filename, image_filename):
    # For each shape object in the LabelMe, extract the label name and the coordinate points and put them into a row list
    shapes = read_in_shapes(lm_path)
    rows = []
    for shape in shapes:
        # row format: reel_filename, image_filename, snip_name, x1, y1, x2...y4
        row = [reel_filename, image_filename]
        row.append(shape["label"]) # snip_name
        for point in shape["points"]:
            row.append(point[0]) # x
            row.append(point[1]) # y
        rows.append(row)
    

        
    

        



if __name__ == "__main__":
    # Command line parameters
    parser = argparse.ArgumentParser(description="Convert a LabelMe file to a .tsv file in snippet generator format")
    parser.add_argument("labelme_filepath", type=str, help="The input file in LabelMe format to be converted to snippet generator format")
    parser.add_argument("output_directory_path", type=str, help="Where to put the output tsv file")
    parser.add_argument("reel_filename", type=str, help="The reel tar file the corresponding image came from. Used to fill the 'reel_filename' column of the output tsv.")
    parser.add_argument("image_filename", type=str, help="The filename of the corresponding image. Used to fill the 'image_filename' column of the output tsv.")

    if len(sys.argv) != 4:
        print('Usage: <labelme_filepath> <output_directory_path> <reel_filename> <image_filename>')
    args = parser.parse_args()

    # Check input file path and type
    lm_path = args.labelme_filepath
    if not os.path.isfile(lm_path):
        raise FileNotFoundError(f"LabelMe file does not exist: {lm_path}")
    CORRECT_EXTENSION = ".json"
    _, file_extension = os.path.splitext(lm_path)
    if file_extension != CORRECT_EXTENSION:
        raise FileNotFoundError(f"File is not a {CORRECT_EXTENSION} file.")

    # Set path to output directory
    out_dir = args.output_directory_path
    if not os.path.isdir(out_dir):
        raise FileNotFoundError(f"Output directory does not exist: {out_dir}")
    print(f'Output set to {out_dir}')

    convert_labelme_to_snippet_generator_format(lm_path, out_dir, args.reel_filename, args.image_filename)


    