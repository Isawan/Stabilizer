import numpy as np
import matplotlib.pyplot as plt
import cv2

def affine_transform(keypoint1,keypoint2,matches):
    src = np.array([keypoint1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
    dst = np.array([keypoint2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)
    affine_matrix = cv2.estimateRigidTransform(src,dst,fullAffine=False)
    transform_matrix = np.zeros((3,3))
    transform_matrix = np.vstack((affine_matrix,[0,0,1]))
    return transform_matrix
