import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from math import sin,sqrt,ceil
import stablizer.util as util
import stablizer.stable as stable
import time

def vid_stitch(filename,mats):
    capture=cv.VideoCapture(filename)
    xmin=min([m[0,2] for m in mats])
    ymin=min([m[1,2] for m in mats])
    mats=mats-np.array([[0,0,xmin],[0,0,ymin],[0,0,0]])
    sx=capture.get(cv.CAP_PROP_FRAME_WIDTH)*sqrt(max([m[0,0]**2+m[1,0]**2 for m in mats]))
    sy=capture.get(cv.CAP_PROP_FRAME_HEIGHT)*sqrt(max([m[0,1]**2+m[1,1]**2 for m in mats]))
    xmax=ceil(max([m[0,2] for m in mats])+sqrt(sx**2+sy**2))#account for rotation and scaling
    ymax=ceil(max([m[1,2] for m in mats])+sqrt(sx**2+sy**2))
    fullIm=np.zeros((ymax,xmax),dtype=np.uint8)
    imFree=np.ones((ymax,xmax),dtype=np.uint8)
    i=0
    ret, f = capture.read()
    while(capture.isOpened()) and ret:
        f = cv.cvtColor(f,cv.COLOR_BGR2GRAY)
        fTrans=cv.warpPerspective(f,mats[i],(xmax,ymax))
        fullIm+=fTrans*imFree
        imFree=np.equal(fullIm,0)
        ret, f = capture.read()
        i+=1
    capture.set(cv.CAP_PROP_POS_FRAMES,0)
    i=0
    ret, f = capture.read()
    writer = util.VideoWriter('example.avi',(ymax,xmax))
    while(capture.isOpened()) and ret:
        f = cv.cvtColor(f,cv.COLOR_BGR2GRAY)
        fTrans=cv.warpPerspective(f,mats[i],(xmax,ymax))
        fImFree=np.equal(fTrans,0)
        fullIm=fTrans+fullIm*fImFree
        writer.write(fullIm)
        ret, f = capture.read()
        print(i)
        i+=1

if __name__ == '__main__':
    video = util.VideoReader('resources/sample2.mp4')
    gmatrices = stable.leapfrog_affine(video)
    vid_stitch('resources/sample2.mp4',gmatrices)
