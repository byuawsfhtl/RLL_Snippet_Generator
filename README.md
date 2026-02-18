# Snippet_Generator
This repository is for the purpose of generating snippets given an image and a json object containing coordinates. It will output a list of snippets to the classifier. 

## Getting Started
### Prerequisites
* PIL
* Numpy
* OpenCV

### Usage

#### Initialization
```python
# Path to tsv file
tsv_file = "objects_on_images.tsv"

# Read the cornerpoints file as a dataframe
objects_df = pd.read_csv(tsv_file, sep='\t)

# Initialize snippet generator by providing a dataframe with the following headers (at least):
    # reel_name, image_name, snip_name, x1, y1, ... x4, y4.
snippet_generator = SnippetGenerator(objects_df)
```

Once initialized, the tool has several functions you can call thusly:

```python 
from snippet_generator import SnippetGenerator
import pandas as pd

# Path to image tar files
images = ["tar_1.tar", "tar_2.tar", "tar_3.tar"]
# Where each tar contains .jpeg files to be snipped

# Path to store the cropped images
output_directory_for_images = "~/cropped_images"

# Save the snippets (cropped images) out to a specified directory
snippet_generator.save_snippets_to_directory_from_image_paths(images, output_directory_for_images)
```
