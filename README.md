# Stablizer

A video stabilizer implementation based on feature point matching by Isawan Millican and Christopher Cole.
The whole project from research, implementation to report was completed in just under two weeks.

Here's an example of the program working.

[![Stablized video](https://img.youtube.com/vi/jjOkjbpqEg/0.jpg)](https://www.youtube.com/watch?v=jjOkjbpqEgA)

The software has been extended to allow image stiching from videos.

![Stiched images](https://isawan.net/fileshare/drone.jpg)


Make sure you have the dependencies installed:
* numpy 
* matplotlib
* skvideo
* opencv
* shapely

So let's start off by generating the mache image. Note -v is optional and assumes 30 fps.

    python3 -m stabilizer.combine -i <input video> -f <output image> -v <start time in secs>:<end time in secs>

Generate the in-frame image

    python3 -m stabilizer.stitch -i <input video> -f <output video>

Generate the normal stablized video (Note: -fm is optional)

    python3 -m stabilizer.stable -i <input video> -f <output video> \
                -fm <matrix print> 

You'll also see compare.py.
That file is used for debugging so you can probably ignore it but for completeness

    python3 -m stabilizer.compare
