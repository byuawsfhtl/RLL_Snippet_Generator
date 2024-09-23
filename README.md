# Snippet_Generator
This repository is for the purpose of generating snippets given an image and a json object containing coordinates. It will output a list of snippets to the classifier. 

## Getting Started
### Prerequisites
* PIL
* Numpy
* OpenCV

### Usage

```python 
from snippet_generator import SnippetGenerator
import pandas as pd

# Path to image tar
images = ["image_1.jpg", "image2.jpg", "image3.jpg"]

# Path to tsv file
tsv_file = "objects_on_images.tsv"

# Path to store the cropped images
output_directory_for_images = "~/cropped_images"

# Read the tsv in as a dataframe
objects_df = pd.read_csv(tsv_file, sep='\t)

# Initialize snippet generator
snippet_generator = SnippetGenerator(objects_df)

# Save the snippets (cropped images) out to a specified directory
snippet_generator.save_snippets_to_directory_from_image_paths(images, output_directory_for_images)
```
