# This script generates test data for the algorithm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpim
from matplotlib import animation
from matplotlib.patches import Circle
from math import sin
from random import randint
#plt.rcParams['animation.ffmpeg_path']='D:\\Apps\\ffmpeg\\ffmpeg-20171031-88c7aa1-win64-static\\bin\\ffmpeg.exe'

dpi = 96
noiseIm= mpim.imread('resources/simnoiseoriginal.png')
fig=plt.figure(figsize=(250/dpi,250/dpi),dpi=dpi)
plt.ion()
im=plt.imshow(noiseIm)
plt.axis('off')
ax=plt.gca()
ax.set_position([0,0,1,1])
circ=Circle((125,175),10)
ax.add_patch(circ)

FFMpegWriter = animation.writers['ffmpeg']
writer=FFMpegWriter(fps=30,bitrate=50000)

with writer.saving(fig,'output/simdata.mp4',dpi*2):
    for i in range(600):
        circ.center= (125+i,175+i+50*sin(i/50))
        r1=randint(-5,5)
        r2=randint(-5,5)
        plt.xlim(i+r1,250+i+r2)
        plt.ylim(50+i+r1+50*sin(i/50),300+i+r2+50*sin(i/50))
        fig.canvas.draw()
        writer.grab_frame()
