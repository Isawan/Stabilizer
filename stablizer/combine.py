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
    if erode:
        kernel = np.ones((3,3),np.uint8)
        for m in range(mask.shape[0]):
            mask[m] = cv2.erode(mask[m].astype(np.uint8),kernel,iterations=1)
            
    for j in range(video.shape[1]):
        for i in range(video.shape[2]):
            ind = mask[:,j,i]
            if not np.any(ind):
                continue
            final[j,i] = func(video[ind,j,i])
    return final


if __name__ == '__main__':
    video = util.loadfile('resources/measure.mp4')[:,::2,::2]
    print(video.shape)
    print('Video loaded')
    stablized_video,info = stable.stablize_video(video,extra=True)
    print('Video stablized')
    print(info['mask'].dtype)
    final = combine_all(stablized_video,info['mask'],np.mean)#,lambda x: x[-1])
    print(final.shape)
    plt.imshow(final,'Greys_r')
    plt.show()
    
