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

# Path to image tar
image_path = "path/to/image.tar"

# Path to json file
json_path = "path/to/json.json"

# Initialize snippet generator
snippet_generator = SnippetGenerator(image_path, json_path)

# Generate snippets from an image and a json object containing coordinates
for img, name in snippet_generator.generate_snippets_from_json(image_path, json_path):
    # Do something with the snippet
    pass
```