import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys
import shapely.geometry as geometry
import stablizer.stable as stable
import stablizer.util as util

# Returns the corners rectangle after being acted on by a perspective transform
# Define shape as (height,width)
def find_corners(shape,tf_matrix):
    assert(len(shape)==2)
    s = shape
    start_rec = np.transpose(((0,0,1),(s[0],0,1),[*s,1],(0,s[1],1)))
    return np.transpose(np.dot(tf_matrix , start_rec)[:2])

def intersect(rect1,rect2):
    a = geometry.Polygon(rect1)
    b = geometry.Polygon(rect2)
    return a.intersection(b)

def combine_all(video,mask,func=np.mean,erode=True):
    final = np.zeros(video.shape[1:])
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
    video = util.loadfile('resources/sample2.mp4')
    print(video.shape)
    print('Video loaded')
    stablized_video,info = stable.stablize_video(video,extra=True)
    print(info['localmt'][10])
    print('Video stablized')
    print(info['mask'].dtype)
    final = combine_all(stablized_video,info['mask'],np.mean)#lambda x: x[-1])
    print(final.shape)
    plt.imshow(final,'Greys_r')
    plt.show()
    
