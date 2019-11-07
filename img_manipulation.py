import cv2
import numpy as np
import PIL
from PIL import Image, ImageEnhance

# Apply brightness in image
#   @param img   - image in rgb format
#   @param alpha - weight of the image
#   @param gamma - scalar added in each sum 
def brightness(img_array, alpha, gamma):
    return cv2.addWeighted(img_array, alpha, np.zeros(img_array.shape, img_array.dtype), 0, gamma)


def exposure(img_array, factor):
    img = Image.fromarray(img_array, 'RGB')
    converter = PIL.ImageEnhance.Color(img)
    img2 = converter.enhance(factor)
    img = np.array(img2)
    return img



#img = cv2.imread("_tempSAIs/4.png")
#img = PIL.Image.open('_tempSAIs/4.png')
'''img = PIL.Image.open('_tempSAIs/4.png')
print(type(img))
converter = PIL.ImageEnhance.Color(img)
img2 = converter.enhance(1.5)
img.show()
img2.show()'''