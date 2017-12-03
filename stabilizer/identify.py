import numpy
import cv2 as cv

def detect_features(image):
    orb = cv.ORB_create()
    return orb.detectAndCompute(image,None)

