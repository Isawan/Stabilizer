import numpy as np
import matplotlib.pyplot as plt
import stablizer.util as util
import stablizer.identify as identify
import cv2

video = util.loadfile('resources/test.mp4')

# Load images
kp    = [0]*2
des   = [0]*2
kp[0],des[0]    = identify.detect_features(video[0])
kp[1],des[0]    = identify.detect_features(video[1])

# Perform matching
bf = cv2.BFMatcher()
print(des[0])
matches = bf.knnMatch(des[0],des[1],k=2)
print(matches)
goodmatches = []
for j,i in matches:
    if j.distance <0.8*i.distance:
        goodmatches.append(j)

# Display
compim= util.combine_compare(video,0,1)
compim = cv2.drawKeypoints(video[0],kp[0],compim,
        color=(255,255,255),flags=cv2.DrawMatchesFlags_DRAW_OVER_OUTIMG)
compim = cv2.drawKeypoints(video[1],kp[1],compim,
        color=(255,255,255),flags=cv2.DrawMatchesFlags_DRAW_OVER_OUTIMG)
plt.imshow(compim/255)
plt.show()
