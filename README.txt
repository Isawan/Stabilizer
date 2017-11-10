Firstly I'm aware I spelt stabilizer wrong in the folder name, but it works so
I won't be trying to change that. 
I'm assuming your using linux but I'm sure you can adapt it to other OSes.
So make sure you have the dependencies installed, I think this is sufficient:
numpy 
matplotlib
skvideo
opencv
shapely

So let's start off by generating the mache image

python3 -m stablizer.combine -i <input video> -f <output image>

Generate the in-frame image

python3 -m stablizer.stitch -i <input video> -f <output video>

Generate the normal stablized video (Note: -fm is optional)

python3 -m stablizer.stable -i <input video> -f <output video> \
                -fm <matrix print> 

You'll also see compare.py. That file is used for debugging you can probably
ignore but for completeness

python3 -m stablizer.compare
