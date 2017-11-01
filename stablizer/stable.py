import numpy as np
import matplotlib.pyplot as plt
import cv2
import stablize.identify as identify
import stablize.match as match
import stablize.transform as transform
import stablize.util as util

def stablize_video(video):
    kp    = [0]*video.shape[0]
    des   = [0]*video.shape[0]
    vid   = [0]*video.shape[0]
    matches = [0]*(video.shape[0]-1)
    invmatr = [0]*(video.shape[0]-1)

    # Identify keypoints and descriptors
    for k in range(video.shape[0]):
        kp[k],des[k] = identify.detect_features(video[k])
    print('Identified keypoints') 

    # Perform matching
    for i in range(1,video.shape[0]):
        matches[i-1] = match.match(kp[i-1],des[i-1],kp[i],des[i])
    print('All matches completed')
    
    # Calculate transformation matrices
    invmatr[i] = np.diag(np.ones(3))
    for i in range(1,video.shape[0]):
        tm = transform.ransac_transform(kp[i-1],kp[i],matches[i-1])
        invmatr[i] = np.linalg.inv()

    # Perform transformations
    for i in range(1,video.shape[0]):
        vid[i] = cv2.warpPerspective(video[i], invmatr[i],
                video[0].shape[-1:1:-1])

    return np.array(vid)

if __name__=='__main__':
    video = util.loadfile('resources/sample1.webm')
