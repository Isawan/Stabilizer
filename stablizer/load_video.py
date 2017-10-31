import cv2 as cv
import numpy as np

def loadfile(filename):
    frames = []
    capture = cv.VideoCapture(filename)
    while(capture.isOpened()):
        ret, f = capture.read()
        frames.append(f)
    return np.array(frames)
