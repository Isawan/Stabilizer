# This file is a scratchspace for testing new algorithms and comparing them
import numpy as np
import matplotlib.pyplot as plt
import stabilizer.util as util
import stabilizer.identify as identify
import stabilizer.match as match
import stabilizer.transform as transform
import stabilizer.drawer as drawer
import cv2


video = util.loadfile('resources/measure.mp4')
print(video.shape)
frame = 697
lag = 697-681

# Load images
kp    = [0]*2
des   = [0]*2
# Feature detection
kp[0],des[0]    = identify.detect_features(video[frame])
kp[1],des[1]    = identify.detect_features(video[frame-lag])

# Perform matching
matches = match.match(kp[0],des[0],kp[1],des[1],maxdist=video.shape[1]/4)
# Dummy gmatrix
gmatp = np.zeros((3,3))
gmat = np.zeros((3,3))
gmat[0,2] = -89
gmat[1,2] = 20
matches = match.clean_direction(gmatp,gmat,kp[1],kp[0],matches)

# Display
compim= util.combine_compare(video[frame],video[frame-lag])

plt.imshow(compim/255)
plt.show()
