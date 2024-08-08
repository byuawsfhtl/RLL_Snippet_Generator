
class CocoHandler:

    def __init__(self) -> None:
        # Dictionary that stores the inputted information in COCO format
        self.coco_dict = {
            "images" : [],
            "annotations" : [],
            "categories" : []
        }
        # Maps from unique identifiers to ids
        self.file_name_to_image_id = {}
        self.name_to_category_id = {}
        # Counters for creating id numbers
        self.next_image_id = 1
        self.next_annotation_id = 1
        self.next_category_id = 1

    def get_or_create_image_entry(self, file_name: str, width: int, height: int) -> int:
        # Throw an error if width or height is invalid
        if not isinstance(width, int) or width < 1:
            raise ValueError(f"Width must be an integer greater than 0. Current value: {width}")
        if not isinstance(height, int) or height < 1:
            raise ValueError(f"Height must be an integer greater than 0. Current value: {height}")

        # If the image is not in the coco dict, add it and assign an id
        if file_name not in self.file_name_to_image_id:
            self.coco_dict["images"].append({
                "id" : self.next_image_id,
                "file_name" : file_name,
                "width" : width,
                "height" : height
                })
            self.file_name_to_image_id[file_name] = self.next_image_id
            self.next_image_id += 1

        # Return the id associated with the file_name
        return self.file_name_to_image_id[file_name]
        
    def create_annotation_entry(self, category_id: int, image_id: int, bbox: list[int]) -> int:
        # Throw an error if the category or image ids are invalid
        if not isinstance(category_id, int) or (category_id < 1) or (category_id >= self.next_category_id):
            raise ValueError(f"Category id is invalid: {category_id}. Current ids are integers assigned in the range [1-{self.next_category_id-1}]")
        if not isinstance(image_id, int) or (image_id < 1) or (image_id >= self.next_image_id):
            raise ValueError(f"Image id is invalid: {image_id}. Current ids are integers assigned in the range [1-{self.next_image_id-1}]")

        self.coco_dict["annotations"].append({
            "id" : self.next_annotation_id,
            "category_id" : category_id,
            "image_id" : image_id,
            "bbox" : bbox
        })
        self.next_annotation_id += 1
        return self.next_annotation_id - 1  # return original number
    
    def get_or_create_category_entry(self, name: str) -> int:
        # If the category is not in the coco dict, add it and assign an id
        if name not in self.name_to_category_id:
            self.coco_dict["categories"].append({
                "id" : self.next_category_id,
                "name" : name
            })
            self.name_to_category_id[name] = self.next_category_id
            self.next_category_id += 1

        # Return the id associated with the category name
        return self.name_to_category_id[name]
    
    def get_coco_dict(self) -> dict:
        return self.coco_dict
    
    


