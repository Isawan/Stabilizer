import numpy as np
import matplotlib.pyplot as plt
import stablizer.util as util
import stablizer.identify as identify
import stablizer.match as match
import stablizer.transform as transform
import stablizer.drawer as drawer
import cv2


video = util.loadfile('resources/measure.mp4')
print(video.shape)
frame = 176
lag = 1

# Load images
kp    = [0]*2
des   = [0]*2
kp[0],des[0]    = identify.detect_features(video[frame])
kp[1],des[1]    = identify.detect_features(video[frame-lag])

# Perform matching
matches = match.match(kp[0],des[0],kp[1],des[1])

# Display
compim= util.combine_compare(video[frame],video[frame-lag])
#compim = cv2.drawKeypoints(video[0],kp[0],compim,
#        color=(255,255,255),flags=cv2.DrawMatchesFlags_DRAW_OVER_OUTIMG)
#compim = cv2.drawKeypoints(video[1],kp[1],compim,
#        color=(255,255,255),flags=cv2.DrawMatchesFlags_DRAW_OVER_OUTIMG)
compim= cv2.drawMatches(video[frame],kp[0],video[frame-lag],kp[1],matches,None)

#tm = transform.affine_transform(kp[0],kp[1],matches)
#invtm = np.linalg.inv(tm)
#vid = cv2.warpPerspective(video[frame-lag],invtm,video[frame].shape[-1::-1])
#compim = util.combine_compare(video[frame],vid)
#src = np.array([kp[0][m.queryIdx].pt for m in matches]).reshape(-1,1,2)
#dst = np.array([kp[1][m.trainIdx].pt for m in matches]).reshape(-1,1,2)
#drawer.draw_matches(src,dst,compim)

plt.imshow(compim/255)
plt.show()
