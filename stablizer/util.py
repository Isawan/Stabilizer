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
def combine_compare(video,shot1,shot2,third=0):
    z = np.ones(video.shape[:2])*third
    return np.stack((video[shot1],z,video[shot2]),axis=2)


