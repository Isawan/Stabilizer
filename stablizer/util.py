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
    def __init__(self,filename,shape):
        assert(len(shape)==2)
        fourcc = cv.VideoWriter_fourcc('X','V','I','D')
        self.vidwriter = cv.VideoWriter(filename,fourcc,30, shape)
        pass

    def write(self,frame):
        self.vidwriter.write(frame)

class VideoShower:
    def __init__(self,window_name):
        self.window_name = window_name
        cv.namedWindow(self.window_name,cv.WINDOW_NORMAL)
        cv.resizeWindow(self.window_name,1200,800)
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

class VideoReader:
    def __init__(self,filename):
        self.filename = filename
        vid = cv.VideoCapture(self.filename)
        self.shape = (
                int(vid.get(cv.CAP_PROP_FRAME_COUNT)),
                int(vid.get(cv.CAP_PROP_FRAME_HEIGHT)),
                int(vid.get(cv.CAP_PROP_FRAME_WIDTH)))
        vid.release()

    def read(self):
        self.capture = cv.VideoCapture(self.filename)

        while self.capture.isOpened():
            ret, frame = self.capture.read()
            if not ret:
                break
            frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
            yield frame
        self.capture.release()

class Video:
    def __init__(self,genfunc,shape):
        self._func = genfunc
        self.shape = shape

    def read(self):
        return self._func()

# Produces a red-blue comparison between two greyscale images
def combine_compare(shot1,shot2):
    assert(shot1.shape == shot2.shape)
    return np.stack((shot1,shot2,shot2),axis=2)
