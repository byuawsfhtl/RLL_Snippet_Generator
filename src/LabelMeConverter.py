'''
This file contains the LabelMeConverter class, which is used to convert LabelMe files to snippet generator format.
LabelMe JSON --> Pandas DataFrame (in Snippet Generator format) --> Output TSV (optional)

When this script is run with command line arguments, LabelMeConverter automatically saves the converted contents to a .tsv file with 
the same name as the LabelMe file.
Usage: <labelme_filepath> <reel_filename> <image_filename> <output_directory_path>

When this module is used within a script, LabelMeConverter can either return a pandas DataFrame or save to a .tsv.
To return a DataFrame, use: convert_to_dataframe(labelme_path, reel_filename, image_filename)
To save to a .tsv, use: convert_to_tsv(labelme_path, reel_filename, image_filename, out_dir)

The information is converted in the following ways:
shape["label"] --> snip_name
shape["points"] --> x1,y1,x2,y2,x3,y3,x4,y4
reel_filename supplied by user
image_filename supplied by user
'''


import os
import sys
import json
import argparse
import pandas as pd


class LabelMeConverter:
    def read_in_shapes(self, labelme_path):
        '''
        This function reads in the LabelMe file and returns the "shapes" list.

        Args:
         labelme_path: filepath to the LabelMe file being converted
        '''
        # Check file exists
        if not os.path.isfile(labelme_path):
            raise FileNotFoundError(f"LabelMe file does not exist: {labelme_path}")
        print('Reading in file...')
        
        # Check file is a JSON file
        CORRECT_EXTENSION = ".json"
        _, file_extension = os.path.splitext(labelme_path)
        if file_extension != CORRECT_EXTENSION:
            raise ValueError(f"File is not a {CORRECT_EXTENSION} file.")

        # Read in file and return the shapes list
        try:
            with open(labelme_path, 'r') as file:
                labelme = json.load(file)
                if labelme['shapes']:
                    return labelme['shapes']
                else:
                    raise ValueError("Shapes list not found in LabelMe file")
        except Exception as e:
            print(f'Error while processing LabelMe file: {e}')


    def convert_to_dataframe(self, labelme_path, reel_filename, image_filename):
        '''
        This function extracts the shapes from a LabelMe file and converts the contents into a pandas DataFrame in snippet generator format.

        Args:
        labelme_path: filepath to the LabelMe file being converted
        reel_filename: the reel tar filename the corresponding image came from. Used to fill the 'reel_filename' column of the output tsv
        image_filename: the filename of the corresponding image. Used to fill the 'image_filename' column of the output tsv
        '''
        # The current snippet generator format has 11 rows
        EXPECTED_ROW_LENGTH = 11
        # For each shape object in the LabelMe, extract the label name and the coordinate points and put them into a row list
        shapes = self.read_in_shapes(labelme_path)
        rows = []
        for shape in shapes:
            # row format: reel_filename, image_filename, snip_name, x1, y1, x2...y4
            row = [reel_filename, image_filename]
            row.append(shape["label"]) # snip_name
            for point in shape["points"]:
                row.append(point[0]) # x
                row.append(point[1]) # y
            row_length = len(row)
            if row_length != EXPECTED_ROW_LENGTH:
                print(f'ERROR: Unsuccessful extraction on current row. Number of columns is {row_length} instead of {EXPECTED_ROW_LENGTH}, so this row will be skipped. Extracted information:')
                print(row)
                continue
            rows.append(row)
        
        df = pd.DataFrame(rows, columns=['reel_filename', 'image_filename', 'snip_name', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4'])
        return df
    
    def convert_to_tsv(self, labelme_path, reel_filename, image_filename, out_dir):
        '''
        This function calls convert_to_dataframe(), then outputs the dataframe to a .tsv file.

        Args:
        labelme_path: filepath to the LabelMe file being converted
        reel_filename: the reel tar filename the corresponding image came from. Used to fill the 'reel_filename' column of the output tsv
        image_filename: the filename of the corresponding image. Used to fill the 'image_filename' column of the output tsv
        out_dir: filepath to the desired output directory (where the .tsv file will be saved)
        '''

        # Check output directory
        if not os.path.isdir(out_dir):
            raise FileNotFoundError(f"Output directory does not exist: {out_dir}")
        print(f'Output set to {out_dir}')

        # Convert the LabelMe to a pandas DataFrame
        df = self.convert_to_dataframe(labelme_path, reel_filename, image_filename)
        # Find output name and path
        input_file_name = os.path.splitext(os.path.basename(labelme_path))[0]
        output_file_name = f'{input_file_name}.tsv'
        output_path = os.path.join(out_dir, output_file_name)
        # Output to tsv
        try:
            df.to_csv(output_path, sep='\t', index=False)
            print(f'LabelMe converted to a .tsv in snippet generator format at {output_path}')
        except Exception as e:
            print(f'ERROR: writing to a .tsv file at {output_file_name} failed with this exception: {e}')



if __name__ == "__main__":
    # Command line parameters
    parser = argparse.ArgumentParser(description="Convert a LabelMe file to a .tsv file in snippet generator format")
    parser.add_argument("labelme_filepath", type=str, help="The input file in LabelMe format to be converted to snippet generator format")
    parser.add_argument("reel_filename", type=str, help="The reel tar file the corresponding image came from. Used to fill the 'reel_filename' column of the output tsv.")
    parser.add_argument("image_filename", type=str, help="The filename of the corresponding image. Used to fill the 'image_filename' column of the output tsv.")
    parser.add_argument("output_directory_path", type=str, help="Where to put the output tsv file")

    if len(sys.argv) != 4:
        print('Usage: <labelme_filepath> <reel_filename> <image_filename> <output_directory_path>')
    args = parser.parse_args()

    # Check input file path and type
    labelme_path = args.labelme_filepath

    # Set path to output directory
    out_dir = args.output_directory_path
    # Instantiate a LabelMeConverter object
    lm_converter = LabelMeConverter()
    # Extract, convert, and output to .tsv
    lm_converter.convert_to_tsv(labelme_path, args.reel_filename, args.image_filename, out_dir)


    