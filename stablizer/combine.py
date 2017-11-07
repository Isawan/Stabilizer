import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys
import shapely.geometry as geometry
import stablizer.stable as stable
import stablizer.util as util


def intersect(rect1,rect2):
    a = geometry.Polygon(rect1)
    b = geometry.Polygon(rect2)
    return a.intersection(b)

def transformed_rect(shape,gmatrix):
    s = shape[1::-1] # Save typing
    rectangle = np.array(( (0,0,1) , (0,s[1],1) , (*s,1) , (s[0],0,1) ))
    return np.einsum('ij...,kj...->ki...',gmatrix,rectangle)[:,:2]

def combine_all(video,mask,func=np.mean,erode=True):
    final = np.zeros(video.shape[1:],np.uint8)
    maskarray = []
    video = np.array(list(video.read()))
    if erode:
        kernel = np.ones((3,3),np.uint8)
        for i,m in enumerate(mask.read()):
            mm = cv2.erode(m,kernel,iterations=1)
            maskarray.append(mm)

    maskarray = np.array(maskarray,dtype=np.bool_)
    for j in range(video.shape[1]):
        for i in range(video.shape[2]):
            ind = maskarray[:,j,i]
            if not np.any(ind):
                continue
            final[j,i] = func(video[ind,j,i])
    return final


if __name__ == '__main__':
    #video = util.loadfile('resources/sample2.mp4')[:,::2,::2]
    video = util.VideoReader('resources/sample2.mp4')
    print(video.shape)
    print('Video loaded')
    stablized_video,info = stable.stablize_video(video,extra=True)
    print('Video stablized')
    final = combine_all(stablized_video,info['mask'],np.mean)#,lambda x: x[-1])
    print(final.shape)
    plt.imshow(final,'Greys_r')
    plt.show()
    
