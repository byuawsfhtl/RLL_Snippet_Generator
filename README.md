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

#Extract the json files from the json tar file into the generator
snippet_generator.extract_json(self.json_tar_path)

#Extract the image files from the image tar file
for image, name in snippet_generator.image_from_tar_generator(image_path):
    #Using each image and its name, generate the snippets
    for snippet, name in snippet_generator.image_snippet_generator(image, name):
        #Do something with the snippet
        pass
```
