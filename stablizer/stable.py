import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys, time
import shapely.geometry as geometry
import stablizer.util as util
import stablizer.identify as identify
import stablizer.match as match
import stablizer.transform as transform
import stablizer.geometry as geometry

# Calculate the required shape of the image given a set of global
# affine transformation matrices and the original shape.
# Also returns the global matrices.
def image_dimensions(shape,gmatrix):
    assert(len(shape) == 2)
    s = shape[1::-1] # Save typing
    rectangle = np.array(( (0,0,1) , (0,s[1],1) , (*s,1) , (s[0],0,1) ))
    trect = np.einsum('ijk...,lk...->ilj...',gmatrix,rectangle)[:,:,:2]
    x = trect[:,:,0]
    y = trect[:,:,1]
    w = np.max(x)-np.min(x)
    h = np.max(y)-np.min(y)

    gm = np.array(gmatrix)
    gm[:,1,2] = gm[:,1,2] - np.min(y)
    gm[:,0,2] = gm[:,0,2] - np.min(x)
    return gm,int(w),int(h)


def frame_affine(keypoints_list,matches_list):
    kp    = keypoints_list
    matches = matches_list
    localmt = np.zeros((len(kp),3,3))
    invmatr = np.zeros((len(kp),3,3))
    gmatrix = np.zeros((len(kp),3,3))

    # Calculate local transformation matrices
    invmatr[0] = np.diag(np.ones(3))
    for i in range(1,len(kp)):
        localmt[i] = transform.affine_transform(kp[i-1],kp[i],matches[i-1])
        invmatr[i] = np.linalg.inv(localmt[i])
    
    # Calculate global transformation matrices
    gmatrix[0] = invmatr[0]
    for i in range(1,len(kp)):
        gmatrix[i] = gmatrix[i-1] @ invmatr[i] 

    return gmatrix

# This algorithm compares each frame against a previous 'fixed' frame.
# As the 'fixed' frame goes out of view, a new fixed frame is generated by
# averaging the last few frames.
def leapfrog_affine(video):
    kp      = [0]*video.shape[0]
    des     = [0]*(len(kp))
    gmatrix = np.zeros((len(kp),3,3))
    gmatrix[0,:,:] = np.diag(np.ones(3))
    
    # Identify keypoints and descriptors
    for k in range(video.shape[0]):
        kp[k],des[k] = identify.detect_features(video[k])
    print('Identified keypoints') 

    f_frame = [0]     # Index of fixed frame, set first frame as initial
    fkp     = [kp[0]] # Key points in fixed frame
    fdes    = [des[0]] # Key points in fixed frame

    for i in range(1,len(kp)):
        try:
            matches = match.match(fkp[-1],fdes[-1],kp[i],des[i],
                    maxdist=video.shape[1]/3)
            localmt = transform.affine_transform(fkp[-1],kp[i],matches)
            gmatrix[i] = gmatrix[f_frame[-1]] @ np.linalg.inv(localmt)
        
        # Fallback on failure
        except (cv2.error,ValueError) as e:
            print(("Error has occured on frame {} with fixed {},"
                    "falling back to frame_affine").format(i,f_frame[-1]))
            print(e)
            matches = match.match(kp[i-1],des[i-1],kp[i],des[i],
                    maxdist=video.shape[1]/4)
            localmt = transform.affine_transform(kp[i-1],kp[i],matches)
            print(gmatrix[i-1])
            print(np.linalg.inv(localmt))
            gmatrix[i] = gmatrix[i-1] @ np.linalg.inv(localmt)



        
        # Calculate frame overlap with fixed frame 
        intersect_area = geometry.intersect(
                geometry.transformed_rect(video.shape[1:],gmatrix[f_frame[-1]]),
                geometry.transformed_rect(video.shape[1:],gmatrix[i])).area
        area = geometry.transformed_rect(video.shape[1:],gmatrix[f_frame[-1]]).area

        if intersect_area/area < 0.75 :
            f_frame.append(i)
            fkp.append(kp[i])
            fdes.append(des[i])

    return gmatrix


  

def stablize_video(video,extra=False):
    kp    = [0]*video.shape[0]
    des   = [0]*video.shape[0]
    matches = [0]*(video.shape[0]-1)
    vid   = [0]*video.shape[0]
    gmatrix = np.zeros((video.shape[0],3,3))

    # Identify keypoints and descriptors
    for k in range(video.shape[0]):
        kp[k],des[k] = identify.detect_features(video[k])
    print('Identified keypoints') 

    # Perform matching
    for i in range(1,video.shape[0]):
        matches[i-1] = match.match(kp[i-1],des[i-1],kp[i],des[i])
    print('All matches completed')
   
    #gmatrix = frame_affine(kp,matches)
    gmatrix = leapfrog_affine(video)
    gmatrix,fx,fy = image_dimensions(video.shape[1:],gmatrix)
    print(fx,fy)
    mask_image = np.ones((video.shape[0],fy,fx),np.bool_)
    base_mask  = np.ones(video.shape[1:],np.uint8)

    # Perform transformations
    for i in range(video.shape[0]):
        vid[i] = cv2.warpPerspective(video[i], gmatrix[i],
                (fx,fy))
        mask_image[i] = cv2.warpPerspective(base_mask, gmatrix[i],
                (fx,fy))
    print('Transformations completed')
    

    if extra:
        extrainfo = {
                'mask':mask_image,
                }
        return np.array(vid),extrainfo

    return np.array(vid)

if __name__=='__main__':
    video = util.loadfile('resources/measure.mp4')[:700,::2,::2]
    print(video.shape)
    stablized_video = stablize_video(video)

    # Prepare video writer
    if '-fs' in sys.argv:
        filename = sys.argv[sys.argv.index('-fs')+1]
        stable_writer = util.VideoWriter(filename,stablized_video.shape[1:]) 
    else:
        stable_writer = util.VideoShower('stable')
   
    for i in range(video.shape[0]):
        print(i)
        stable_writer.write(stablized_video[i])
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
