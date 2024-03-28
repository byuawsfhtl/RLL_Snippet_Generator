'''
File: filename.py
Danny Wright
Description: 
Get some images in a zip or tar
Get JSON files of segmented images
Instantiate Snippet generator
Get gender snippets only
Pass snippets into machine learning model (classifier class)
Instantiate classifier
'''

# imports
import snippet_generator

class SampleClass:
    """Sample class to demonstrate structure."""

    def __init__(self, parameter):
        self.parameter = parameter

    def sample_method(self):
        """Sample method that does something."""
        pass


def sample_function(argument):
    """Sample function that does something.

    Args:
        argument (type): Description of argument.

    Returns:
        type: Description of return value.
    """
    return argument


def main():
    """Main function that orchestrates everything."""
    # Example usage of a function
    result = sample_function("Hello, World!")
    print(result)

    # Example usage of a class
    example = SampleClass("Example")
    example.sample_method()


if __name__ == "__main__":
    main()
