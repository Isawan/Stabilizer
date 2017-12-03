import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys
import shapely.geometry as geometry
import stabilizer.stable as stable
import stabilizer.util as util


# A simple stiching of frames to form a large image.
# Computes overlapping pixels using the func parameter, set to mean as default.
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

# Mache drawing, a method of stiching that only puts stiches an image in when the
# overlap between frames falls below a threshold.
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
    assert('-f' in sys.argv)
    assert('-i' in sys.argv)
    if '-v' in sys.argv: 
        ran = sys.argv[sys.argv.index('-v')+1]
        mint,maxt = map(float,ran.split(':'))
        video = util.VideoReader(sys.argv[sys.argv.index('-i')+1],
                minframe=int(mint*30),maxframe=int(maxt*30))
    else:
        video = util.VideoReader(sys.argv[sys.argv.index('-i')+1])
    print(video.shape)
    print('Video loaded')
    stabilized_video,info = stable.stabilize_video(video,extra=True)
    print('Video stabilized')
    #final = combine_all(stabilized_video,info['mask'],np.mean)#,lambda x: x[-1])
    final = mache(video,info['gmatrix'])
    print(final.shape)
    #cv2.imwrite('output/measure.bmp',final)
    plt.imsave(sys.argv[sys.argv.index('-f')+1],final,cmap='Greys_r')
    
