import os
import sys
import json
import argparse
import pandas as pd

from labelme_converter import LabelMe_Converter

#from groups.fslg_census.nobackup.archive.common_tools.snippet_generator.branches.Sarah.RLL_Snippet_Generator.src.labelme_converter.LabelMe_Converter import LabelMe_Converter
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

LABELME="/home/sks239/groups/fslg_census/nobackup/archive/common_tools/snippet_generator/branches/Sarah/RLL_Snippet_Generator/tests/test_labelme_converter/test_labelme.json"
REEL_NAME="test_reel_name_000.tar"
IMAGE_NAME="test_image_name_000.jpg"

converter = LabelMe_Converter()
df = converter.convert_labelme_to_snippet_generator_format(LABELME, REEL_NAME, IMAGE_NAME)
print(df)


