import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys
import stablizer.util as util
import stablizer.identify as identify
import stablizer.match as match
import stablizer.transform as transform

def stablize_video(video,output_matrix=False):
    kp    = [0]*video.shape[0]
    des   = [0]*video.shape[0]
    matches = [0]*(video.shape[0]-1)
    vid   = [0]*video.shape[0]
    localmt = np.zeros((video.shape[0],3,3))
    invmatr = np.zeros((video.shape[0],3,3))
    gmatrix = np.zeros((video.shape[0],3,3))

    # Identify keypoints and descriptors
    for k in range(video.shape[0]):
        kp[k],des[k] = identify.detect_features(video[k])
    print('Identified keypoints') 

    # Perform matching
    for i in range(1,video.shape[0]):
        matches[i-1] = match.match(kp[i-1],des[i-1],kp[i],des[i])
    print('All matches completed')
    
    # Calculate local transformation matrices
    invmatr[0] = np.diag(np.ones(3))
    for i in range(1,video.shape[0]):
        localmt[i] = transform.affine_transform(kp[i-1],kp[i],matches[i-1])
        invmatr[i] = np.linalg.inv(localmt[i])
    print('Calculated local transformation matrices')

    # Calculate global transformation matrices
    gmatrix[0] = invmatr[0]
    for i in range(1,video.shape[0]):
        gmatrix[i] = gmatrix[i-1] @ invmatr[i] 

    # Calculate final size
    fx = (np.max(gmatrix[:,0,2])-np.min(gmatrix[:,0,2])
            + video.shape[2]).astype(int)
    fy = (np.max(gmatrix[:,1,2])-np.min(gmatrix[:,1,2])
            + video.shape[1]).astype(int)

    # Perform transformations
    for i in range(video.shape[0]):
        vid[i] = cv2.warpPerspective(video[i], gmatrix[i],
                (fx,fy))
    print('Transformations completed')

    if output_matrix :
        return np.array(vid),localmt
    return np.array(vid)

if __name__=='__main__':
    video = util.loadfile('resources/sample2.mp4')[60:]
    stablized_video = stablize_video(video)

    # Prepare video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    if '-fs' in sys.argv:
        filename = sys.argv[sys.argv.indexOf('-ft')+1]
        stable_writer = util.VideoWriter(filename) 
    else:
        stable_writer = util.VideoShower('stable')
   
    if '-fm' in sys.argv:
        matrix_writer = util.MatrixWriter()
    else:
        matrix_writer = util.DummyWriter()

    for i in range(video.shape[0]):
        stable_writer.write(stablized_video[i])
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
