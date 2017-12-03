I'm assuming your using linux but I'm sure you can adapt it to other OSes.
So make sure you have the dependencies installed, I think this is sufficient:
numpy 
matplotlib
skvideo
opencv
shapely
python3.5

So let's start off by generating the mache image. Note -v is optional and assumes 30 fps.

python3 -m stablizer.combine -i <input video> -f <output image> -v <start time in secs>:<end time in secs>

Generate the in-frame image

python3 -m stablizer.stitch -i <input video> -f <output video>

Generate the normal stablized video (Note: -fm is optional)

python3 -m stablizer.stable -i <input video> -f <output video> \
                -fm <matrix print> 

You'll also see compare.py. That file is used for debugging you can probably
ignore but for completeness

python3 -m stablizer.compare
