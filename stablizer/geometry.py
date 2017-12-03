import numpy as np
import shapely.geometry as geometry

# Wrapper to calculate intersection of rectangles defined by corners coordinates.
def intersect(shape1,shape2):
    return shape1.intersection(shape2)

# Batch transformation to a list of rectangles under a matrix.
def transformed_rect(shape,gmatrix):
    s = shape[1::-1] # Save typing
    rectangle = np.array(( (0,0,1) , (0,s[1],1) , (*s,1) , (s[0],0,1) ))
    return geometry.Polygon(np.einsum('ij...,kj...->ki...',
        gmatrix,rectangle)[:,:2])
