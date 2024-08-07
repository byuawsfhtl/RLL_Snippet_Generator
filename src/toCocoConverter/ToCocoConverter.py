import os
import sys
import json
import argparse
import logging
import pycocotools

# Create a logger and send output to stdout
logger = logging.getLogger('output_logger')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

