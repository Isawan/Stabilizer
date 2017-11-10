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

def mache(video,gmatrices,overlap=0.9):
    s = video.shape[-1:0:-1]
    rectangle = np.array(( (0,0,1) , (0,s[1],1) , (*s,1) , (s[0],0,1) ))
    trect = np.einsum('ijk...,lk...->ilj...',gmatrices,rectangle)[:,:,:2]
    keepidx = [0]
    keep = [trect[0]]
    _,w,h = stable.image_dimensions(video.shape[1:],gmatrices)
    portrait = np.zeros((h,w),np.uint8)

    for i,r in enumerate(trect[1:]):
        area = geometry.Polygon(keep[-1]).area
        intersect_area = geometry.Polygon(r).intersection(geometry.Polygon(keep[-1])).area
        if intersect_area/area < overlap:
            keep.append(r)
            keepidx.append(i)

    base_mask = np.ones(video.shape[1:],np.uint8)
    kernel = np.ones((5,5),np.uint8)
    for i,frame in enumerate(video.read()):

        mask = np.zeros((h,w),np.uint8)
        mask = cv2.warpPerspective(base_mask,gmatrices[i],(w,h))
        mask = cv2.erode(mask,kernel,iterations=1)
        mask = mask.astype(np.bool_)

        part = cv2.warpPerspective(frame,gmatrices[i],(w,h))
        portrait[mask] = part[mask]

    for i,frame in enumerate(video.read()):
        if i not in keepidx:
            continue

        mask = np.zeros((h,w),np.uint8)
        mask = cv2.warpPerspective(base_mask,gmatrices[i],(w,h))
        mask = cv2.erode(mask,kernel,iterations=1)
        mask = mask.astype(np.bool_)

        part = cv2.warpPerspective(frame,gmatrices[i],(w,h))
        portrait[mask] = part[mask]

    return portrait
    


if __name__ == '__main__':
    video = util.VideoReader('output/simdata.mp4')
    print(video.shape)
    print('Video loaded')
    stablized_video,info = stable.stablize_video(video,extra=True)
    print('Video stablized')
    #final = combine_all(stablized_video,info['mask'],np.mean)#,lambda x: x[-1])
    final = mache(video,info['gmatrix'])
    print(final.shape)
    #cv2.imwrite('output/measure.bmp',final)
    plt.imsave('output/simnoise.png',final,cmap='Greys_r')
    
