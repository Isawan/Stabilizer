import cv2 as cv
import numpy as np

def loadfile(filename,maxframe=None):
    frames = []
    capture = cv.VideoCapture(filename)
    fc = 0
    while(capture.isOpened()):
        ret, f = capture.read()
        if not ret:
            break
        f = cv.cvtColor(f,cv.COLOR_BGR2GRAY)
        frames.append(f)
        if maxframe and fc >= maxframe:
            break
        fc = fc + 1
    return np.array(frames)

class VideoWriter:
    def __init__(self,filename):
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        self.vidwriter = cv.VideoWriter(filename,fourcc,30,
                stablized_video.shape[-1:0:-1])
        pass

    def write(self,frame):
        self.vidwriter.write(frame)

class VideoShower:
    def __init__(self,window_name):
        self.window_name = window_name
    def write(self,frame):
        cv.imshow(self.window_name,frame)

class TextWriter:
    def __init__(self,file_name):
        self.filename = file_name

    def write(self,text):
        with open(self.filename,'w') as f:
            f.write(text)

class TextShower:
    def write(self,text):
        print(text)

class MatrixWriter:
    def __init__(self,file_name):
        self.filename = file_name

    def write(self,matrix):
        np.save(matrix)

class DummyWriter:
    def write(self,something):
        pass


# Produces a red-blue comparison between two greyscale images
def combine_compare(shot1,shot2,third=0):
    assert(shot1.shape == shot2.shape)
    z = np.ones(shot1.shape[:2])*third
    return np.stack((shot1,z,shot2),axis=2)
