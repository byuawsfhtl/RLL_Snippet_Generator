import os
import sys
import json
import argparse
import logging
import pycocotools

from CocoHandler import CocoHandler
#current = os.path.dirname(os.path.realpath(__file__))


# Create a logger and send output to stdout
logger = logging.getLogger('output_logger')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

class ToCocoConverter:
    def __init__(self):
        self.coco = CocoHandler()

    def convert(self, input_path, output_dir):
        # Check input file exists
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Snippet Generator file does not exist at given path: {input_path}")
        logger.info('Input file located')
        # Check file is a .tsv
        CORRECT_EXTENSION = ".tsv"
        _, file_extension = os.path.splitext(input_path)
        if file_extension != CORRECT_EXTENSION:
            raise TypeError(f"LabelMe file parameter extension is '{file_extension}'; expected '{CORRECT_EXTENSION}'")

        # Verify output directory
        if not os.path.isdir(output_dir):
            raise FileNotFoundError(f"Output directory does not exist: {output_dir}")
        logger.info(f'Output set to {output_dir}')
