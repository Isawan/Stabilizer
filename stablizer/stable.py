import numpy as np
import matplotlib.pyplot as plt
import cv2
import stablizer.util as util
import stablizer.identify as identify
import stablizer.match as match
import stablizer.transform as transform

def stablize_video(video):
    kp    = [0]*video.shape[0]
    des   = [0]*video.shape[0]
    vid   = [0]*video.shape[0]
    matches = [0]*(video.shape[0]-1)
    invmatr = [0]*(video.shape[0])

    # Identify keypoints and descriptors
    for k in range(video.shape[0]):
        kp[k],des[k] = identify.detect_features(video[k])
    print('Identified keypoints') 

    # Perform matching
    for i in range(1,video.shape[0]):
        matches[i-1] = match.match(kp[i-1],des[i-1],kp[i],des[i])
    print('All matches completed')
    
    # Calculate transformation matrices
    invmatr[0] = np.diag(np.ones(3))
    for i in range(1,video.shape[0]):
        tm = transform.ransac_transform(kp[i-1],kp[i],matches[i-1])
        invmatr[i] = np.linalg.inv(tm)
    print('Calculated transformation matrices')

    # Perform transformations
    for i in range(video.shape[0]):
        vid[i] = cv2.warpPerspective(video[i], invmatr[i],
                video[0].shape[-1::-1])
    print('Transformations completed')
    
    return np.array(vid)

if __name__=='__main__':
    video = util.loadfile('resources/sample2.mp4')
    print(video.shape)
    stablized_video = stablize_video(video)
    for i in range(video.shape[0]):
        com = util.combine_compare(video[i],stablized_video[i])
        cv2.imshow('compare',com/255)
        #cv2.imshow('video',video[i])
        #cv2.imshow('stable',stablized_video[i])
        if cv2.waitKey(500) & 0xFF == ord('q'):
            break
