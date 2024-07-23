#!/bin/bash

LABELME="/home/sks239/groups/fslg_census/nobackup/archive/common_tools/snippet_generator/branches/Sarah/RLL_Snippet_Generator/tests/test_labelme_converter/test_labelme.json"
REEL_NAME="test_reel_name_000.tar"
IMAGE_NAME="test_image_name_000.jpg"
OUTPUT_DIRECTORY="/home/sks239/groups/fslg_census/nobackup/archive/common_tools/snippet_generator/branches/Sarah/RLL_Snippet_Generator/tests/test_labelme_converter"

python /home/sks239/groups/fslg_census/nobackup/archive/common_tools/snippet_generator/branches/Sarah/RLL_Snippet_Generator/src/labelme_converter.py $LABELME $REEL_NAME $IMAGE_NAME $OUTPUT_DIRECTORY
