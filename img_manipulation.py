import cv2
import numpy as np

# Apply brightness in image
#   @param img   - image in rgb format
#   @param alpha - weight of the image
#   @param gamma - scalar added in each sum 
def brightness(img, alpha, gamma):
    return cv2.addWeighted(img, alpha, np.zeros(img.shape, img.dtype), 0, gamma)
