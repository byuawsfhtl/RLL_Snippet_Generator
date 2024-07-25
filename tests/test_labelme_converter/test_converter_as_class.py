import os
import sys
import json
import argparse
import pandas as pd

# TODO: figure out how to fix the import...
current = os.path.dirname(os.path.realpath(__file__))
testFolder = os.path.dirname(current)
root = os.path.dirname(testFolder)
sys.path.append(os.path.join(root, "src"))

from LabelMeConverter import LabelMeConverter

LABELME="/home/sks239/groups/fslg_census/nobackup/archive/common_tools/snippet_generator/branches/Sarah/RLL_Snippet_Generator/tests/test_labelme_converter/test_labelme.json"

REEL_NAME="test_reel_name_000.tar"
IMAGE_NAME="test_image_name_000.jpg"

converter = LabelMeConverter()
df = converter.convert_to_dataframe(LABELME, REEL_NAME, IMAGE_NAME)
print(df)


