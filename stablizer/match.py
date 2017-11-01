import numpy as np
import cv2

# Returns a dict that maps keypoint1 -> keypoint2
# Not all keypoints are garunteed to be mapped
def match(keypoint1,descriptor1,keypoint2,descriptor2):
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(descriptor1,descriptor2,k=2)
    good = []
    for m,n in matches:
        if m.distance < 0.8*n.distance:
            good.append(m)
    return sorted(good,key=lambda x:x.distance)

