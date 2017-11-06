import numpy as np
import cv2
import itertools

# Returns a dict that maps keypoint1 -> keypoint2
# Not all keypoints are garunteed to be mapped
def match(keypoint1,descriptor1,keypoint2,descriptor2,maxdist=300,ratio=0.8):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(descriptor1,descriptor2,k=2)
    good = []
    prox = []
    # Apply ratio test
    for m,n in matches:
        if m.distance < ratio*n.distance:
            good.append(m)

    ## Proximity test
    #for m in good:
    #    dist = np.linalg.norm(np.array(keypoint1[m.queryIdx].pt)-
    #            np.array(keypoint2[m.trainIdx].pt))
    #    if dist < maxdist:
    #        prox.append(m)

    return sorted(good,key=lambda x:x.distance)

# Tries to remove matches pointing in opposite direction to camera movement.
def clean_direction(gmprev,gmcur,keypoint1,keypoint2,matches,maxchange=100):
    # Extract spatial shift information from gmatrix
    dx = gmcur[0,2] - gmprev[0,2]
    dy = gmcur[1,2] - gmprev[1,2]
    print(dx,dy)

    # Filter
    # Check that the matching vector is within a spatial square centred on
    # the previous frame translation
    x = np.array([(keypoint2[m.queryIdx].pt[0]
        - keypoint1[m.trainIdx].pt[0]) for m in matches])
    matches = list(itertools.compress(matches,
        np.all([x > (dx - maxchange),x < (dx + maxchange)],axis=0)))
    y = np.array([(keypoint2[m.queryIdx].pt[1]
        - keypoint1[m.trainIdx].pt[1]) for m in matches])
    matches = list(itertools.compress(matches,
        np.all([y > (dy - maxchange),y < (dy + maxchange)],axis=0)))
    return matches


