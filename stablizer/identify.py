import numpy
import cv2 as cv

def detect_features(image):
    sift = cv.xfeatures2d.SIFT_create()
    kp = sift.detect(image,None)
    return kp

