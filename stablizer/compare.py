import numpy as np
import matplotlib.pyplot as plt
import stablizer.util as util
import stablizer.identify as identify
import stablizer.match as match
import stablizer.transform as transform
import cv2

video = util.loadfile('resources/sample1.webm')

# Load images
kp    = [0]*2
des   = [0]*2
kp[0],des[0]    = identify.detect_features(video[0])
kp[1],des[1]    = identify.detect_features(video[10])

# Perform matching
m = match.match(kp[0],des[0],kp[1],des[1])

# Display
#compim= util.combine_compare(video,0,1)
#compim = cv2.drawKeypoints(video[0],kp[0],compim,
#        color=(255,255,255),flags=cv2.DrawMatchesFlags_DRAW_OVER_OUTIMG)
#compim = cv2.drawKeypoints(video[1],kp[1],compim,
#        color=(255,255,255),flags=cv2.DrawMatchesFlags_DRAW_OVER_OUTIMG)
#compim= cv2.drawMatches(video[0],kp[0],video[10],kp[1],m,None)
tm = transform.ransac_transform(kp[0],kp[1],m)
invtm = np.linalg.inv(tm)
vid = cv2.warpPerspective(video[10],invtm,video[0].shape[-1::-1])
compim = util.combine_compare(video[0],video[10])

plt.imshow(compim/255)
plt.show()
