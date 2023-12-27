import cv2 as cv
import numpy as np

haystack = cv.imread('farm.png', cv.IMREAD_UNCHANGED)
needle = cv.imread('cabbage.png', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(haystack, needle, cv.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

threshhold = 0.8
if max_val >= threshhold:
    print('Found needle')
    
    needle_w = needle.shape[1]
    needle_h = needle.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0]+needle_w, top_left[1]+needle_h)

    cv.rectangle(haystack, top_left, bottom_right, color=(0,255,0), thickness=2, lineType=cv.LINE_4)

    cv.imshow('Result', haystack)
    cv.waitKey()

else:
    print('Not Found')
