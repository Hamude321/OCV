import cv2 as cv
import numpy as np


def findClickPositions(needle_img_path, haystack_img, threshhold=0.5, debug_mode=None):

    needle = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

    needle_w = needle.shape[1]
    needle_h = needle.shape[0]

    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(haystack_img, needle, method)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    threshhold = 0.4
    locations = np.where(result>=threshhold)
    locations = list(zip(*locations[::-1]))

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
    print(rectangles)

    points = []
    if len(rectangles):
        print('Found')

        line_color = (0,255,0)
        line_type = cv.LINE_4
        marker_color = (255,0,0)
        marker_type = cv.MARKER_CROSS

        for (x, y, w, h) in rectangles:
            center_x = x + int(w/2)
            center_y = y + int(h/2)

            points.append((center_x, center_y))

            if debug_mode == 'rectangles':               
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
            elif debug_mode == 'points':            
                 cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

    if debug_mode:
        cv.imshow('Matches', haystack_img)
        #cv.waitKey()

    return points


#points = findClickPositions('cabbage.png', 'farm.png', debug_mode='rectangles')