import cv2 as cv
import numpy as np

class Interface:

    TRACKBAR_WINDOW = "Trackbars"
    threshold = 0

    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.
        def nothing(position):
            pass

        # create trackbars for bracketing.
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('Threshold', self.TRACKBAR_WINDOW, 30, 100, nothing)

        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('Threshold', self.TRACKBAR_WINDOW, 70)


    # returns an HSV filter object based on the control GUI values
    def get_threshold_from_bar(self):
        self.threshold = cv.getTrackbarPos('Threshold', self.TRACKBAR_WINDOW)/100
        if self.threshold<0.3:
            self.threshold=0.3
        #print(self.threshold)
        return self.threshold
