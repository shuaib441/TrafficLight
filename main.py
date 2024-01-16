import os
import cv2
import numpy as np


def detect(filepath, file):
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.imread(filepath+file)
    cimg = img
    hsv = cv2.cvtcolor(img, cv2.COLOR_BGR2HSV)

    lower_rad1 = np.array([0,100,100])
    upper_rad1 = np.array([10,255,255])
    lower_rad2 = np.array([160,100,100])
    