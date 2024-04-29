import os
from PIL import Image
    
def resize_image(image):            ## This is actually expecting the file path to that "image"
    try:
        img_object = Image.open(image)
        print(f"Image opened: {image}")
        print(img_object.size)
        newsize = [400,400]
        resized_img = img_object.resize(newsize)
        resized_img.save(image)
        return resized_img
    except OSError:
            print(f"Error opening image: {image}")