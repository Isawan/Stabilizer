import cv2

def draw_matches(src,dst,image,color=0x00ff00):
    assert(len(src)==len(dst))
    for i in range(len(src)):
        cv2.arrowedLine(image,
                tuple(src[i,0].astype(int)),
                tuple(dst[i,0].astype(int)),
                color,line_type=4)
    
