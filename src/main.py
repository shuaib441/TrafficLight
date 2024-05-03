#!/usr/bin/env python
# coding: utf-8
# created by hevlhayt@foxmail.com 
# Date: 2016/1/15 
# Time: 19:20
#
import os
import cv2
import numpy as np


def detect(filepath, file):
# initializes a font and reads an image using OpenCV's cv2.imread function. 
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.imread(filepath+file)
    cimg = img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # color range
    #defining color ranges using NumPy arrays for both red and green colors in the HSV color space
    #These ranges are commonly used in image processing tasks to filter specific colors within an image.
    lower_red1 = np.array([0,100,100])
    upper_red1 = np.array([10,255,255])
    lower_red2 = np.array([160,100,100])
    upper_red2 = np.array([180,255,255])
    lower_green = np.array([40,50,50])
    upper_green = np.array([90,255,255])
    # lower_yellow = np.array([15,100,100])
    # upper_yellow = np.array([35,255,255])
    lower_yellow = np.array([15,150,150])
    upper_yellow = np.array([35,255,255])
    # creating masks for specific color ranges in the HSV color space using OpenCV's cv2.inRange function.
    # The masks are created for red, green, and potentially yellow colors
    #Mask for the first part of the red color range (lower_red1 to upper_red1).
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    # Mask for the second part of the red color range (lower_red2 to upper_red2).
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    maskg = cv2.inRange(hsv, lower_green, upper_green)
    masky = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # Combined mask for red color by adding mask1 and mask2.
    maskr = cv2.add(mask1, mask2)

    size = img.shape
    # print size

    # hough circle detect
    #using the Hough Circle Transform in OpenCV (cv2.HoughCircles) to detect circles in the maskr image.
    #maskr: The input image (grayscale) where circles are to be detected.
    #cv2.HOUGH_GRADIENT: The method used for circle detection. 
    #1: The inverse ratio of the accumulator resolution to the image resolution. it means the accumulator has the same resolution as the input image.
    #80: The minimum distance between the centers of detected circles. If the distance between the centers of two circles is less than this value, then the smaller circle is discarded.
    #param1=50: The higher threshold of the two passed to the Canny edge detector. It is used to find edges in the input image.
    #param2=10: The accumulator threshold for the circle centers at the detection stage. A smaller value will lead to more detected circles, but some false circles may be included.
    #minRadius=0: The minimum radius of the circles to be detected.
    #maxRadius=30: The maximum radius of the circles to be detected.


    
    r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80,
                               param1=50, param2=10, minRadius=0, maxRadius=30)

    g_circles = cv2.HoughCircles(maskg, cv2.HOUGH_GRADIENT, 1, 60,
                                 param1=50, param2=10, minRadius=0, maxRadius=30)

    y_circles = cv2.HoughCircles(masky, cv2.HOUGH_GRADIENT, 1, 30,
                                 param1=50, param2=5, minRadius=0, maxRadius=30)

    # traffic light detect
    #It looks like you are setting some parameters, such as the radius (r), a boundary (bound), and then checking if circles were detected
    # (if r_circles is not None). If circles are detected, you are rounding the circle coordinates to integers using np.around and converting them to np.uint16.
    r = 5
    bound = 4.0 / 10
    if r_circles is not None:
        r_circles = np.uint16(np.around(r_circles))

    #This code appears to be iterating through the detected circles (r_circles) and performing some additional processing for each circle.    
    #The loop iterates through each detected circle (i) in r_circles.

        for i in r_circles[0, :]:
    # checks whether the circle's coordinates exceed the image size or a specified boundary (bound). If the condition is met, the loop skips to the next iteration.        
            if i[0] > size[1] or i[1] > size[0]or i[1] > size[0]*bound:
                continue
    #Inside the loop, there's a nested loop that iterates over a square neighborhood of the circle with a radius of r.
    #The nested loop accumulates the values in the maskr image within the neighborhood of each circle.
            h, s = 0.0, 0.0
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                        continue
                    h += maskr[i[1]+m, i[0]+n]
                    s += 1
            if h / s > 50:
                cv2.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                cv2.circle(maskr, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                cv2.putText(cimg,'RED',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)

    if g_circles is not None:
        g_circles = np.uint16(np.around(g_circles))

        for i in g_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
                continue

            h, s = 0.0, 0.0
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                        continue
                    h += maskg[i[1]+m, i[0]+n]
                    s += 1
                   
            if h / s > 100:
                cv2.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                cv2.circle(maskg, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                cv2.putText(cimg,'GREEN',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)

    if y_circles is not None:
        y_circles = np.uint16(np.around(y_circles))

        for i in y_circles[0, :]:
            if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
                continue

            h, s = 0.0, 0.0
            for m in range(-r, r):
                for n in range(-r, r):

                    if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                        continue
                    h += masky[i[1]+m, i[0]+n]
                    s += 1
     #If the average value (h / s) in the neighborhood is greater than 50, it is considered a significant region,
    # and the code proceeds to draw a green circle around the detected circle, a white circle in the maskr image, 
    # and adds the label "RED" to the original image (cimg).                
            if h / s > 50:
                cv2.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                cv2.circle(masky, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                cv2.putText(cimg,'YELLOW',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)

    cv2.imshow('detected results', cimg)
    cv2.imwrite(path+'//result//'+file, cimg)
    # cv2.imshow('maskr', maskr)
    # cv2.imshow('maskg', maskg)
    # cv2.imshow('masky', masky)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':

    path = os.path.abspath('..')+'//light//'
    #path="C:/Maitexa1/projects/safi/TrafficLight/src/light"
    for f in os.listdir(path):
        print (f)
        if f.endswith('.jpg') or f.endswith('.JPG') or f.endswith('.png') or f.endswith('.PNG'):
            detect(path, f)

