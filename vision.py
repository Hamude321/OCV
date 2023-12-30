import cv2 as cv
import numpy as np
import pyautogui
from time import sleep
import cv2
from threading import Thread, Lock


class Vision:

    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    # threading properties
    stopped = True
    lock = None
    rectangles = []
    # properties
    screenshot = None
    detection_img = None


    # constructor
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.lock = Lock()
        # load the image we're trying to match
        # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        # Save the dimensions of the needle image
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def find(self, haystack_img, threshhold=0.4, max_results=10):

        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        locations = np.where(result>=threshhold)
        locations = list(zip(*locations[::-1]))

        if not locations:
            return np.array([], dtype=np.int32).reshape(0,4)

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
        print(rectangles)

        if len(rectangles) > max_results:
            print('Warning: Too many results, raise threshold')
            rectangles = rectangles[:max_results]
        

        return rectangles

    def get_click_points(self, rectangles):
        points = []

        for (x, y, w, h) in rectangles:
            center_x = x + int(w/2)
            center_y = y + int(h/2)

            points.append((center_x, center_y))
        return points


    def draw_rectangles(self, haystack_img, rectangles):
        line_color = (0,255,0)
        line_type = cv.LINE_4
    
        for (x,y,w,h) in rectangles:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)
        return haystack_img

    def draw_crosshairs(self, haystack_img, points):
        marker_color=(255,0,255)
        marker_type=cv.MARKER_CROSS
        for (center_x, center_y) in points: 
             cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)
        return haystack_img
    


    def update_rectangles(self, rectangles):
        self.lock.acquire()
        self.rectangles = rectangles
        self.lock.release()

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            if not self.screenshot is None:
                if not self.rectangles is None:
                    # do object detection
                    detection_img = self.draw_rectangles(self.screenshot, self.rectangles)
                    # lock the thread while updating the results
                    self.lock.acquire()
                    self.detection_img = detection_img
                    self.lock.release()