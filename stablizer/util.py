import cv2 as cv
import numpy as np

def loadfile(filename):
    frames = []
    capture = cv.VideoCapture(filename)
    while(capture.isOpened()):
        ret, f = capture.read()
        if not ret:
            break
        f = cv.cvtColor(f,cv.COLOR_BGR2GRAY)
        frames.append(f)
    return np.array(frames)

# Produces a red-blue comparison between two greyscale images
def combine_compare(shot1,shot2,third=0):
    assert(shot1.shape == shot2.shape)
    z = np.ones(shot1.shape[:2])*third
    return np.stack((shot1,z,shot2),axis=2)


