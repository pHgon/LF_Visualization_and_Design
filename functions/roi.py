import qimage2ndarray
from . import utils 
import numpy as np
import cv2

import matplotlib.pyplot as plt
  

def roi_espiral(matrix_SAIs):
    img_array = []

    for tupla in utils.roi_espiral:
        img_array.append(matrix_SAIs[tupla[0]][tupla[1]])

    first_gray = cv2.cvtColor(img_array[0], cv2.COLOR_BGR2GRAY)
    first_gray = cv2.GaussianBlur(first_gray, (5,5), 0)
    #cv2.imwrite("0.png", img_array[0])

    diffs = []
    for index, frame in enumerate(img_array):
        if index != 0:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame, (3, 3), 0)

            difference = cv2.absdiff(first_gray, gray_frame)
            _, difference = cv2.threshold(difference, 15, 255, cv2.THRESH_BINARY)

            #cv2.imwrite("Frames/" + str(index) + ".png", frame)
            diffs.append(difference)

    return diffs, img_array[1:]

    # subtractor = cv2.createBackgroundSubtractorMOG2(history=80, varThreshold=10, detectShadows=True)

    # for index, frame in enumerate(img_array):
    #     mask = subtractor.apply(frame)


    #     cv2.imwrite("Frames/" + str(index) + ".png", frame)
    #     cv2.imwrite("Masks/" + str(index) + "dif.png", mask)

