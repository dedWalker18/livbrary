import os
from PIL import Image
    
def resize_image(image):                            ## path to image expected!!
    try:
        img_object = Image.open(image)
        newsize = [400,400]
        resized_img = img_object.resize(newsize)
        resized_img.save(image)
        return resized_img
    except OSError:
            print(f"Error opening image: {image}")
