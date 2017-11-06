import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys

def affine_transform(keypoint1,keypoint2,matches):
    src = np.array([keypoint1[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
    dst = np.array([keypoint2[m.trainIdx].pt for m in matches]).reshape(-1,1,2)
    try:
        affine_matrix = cv2.estimateRigidTransform(src,dst,fullAffine=False)
        transform_matrix = np.zeros((3,3))
        transform_matrix = np.vstack((affine_matrix,[0,0,1]))
    except ValueError as e:
        raise ValueError('Not enough feature points') from e
    except cv2.error as e:
        raise cv2.error('Image too noisy') from e

    return transform_matrix
