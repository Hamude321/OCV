import cv2 as cv
import numpy as np
import os
from detection import Detection
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
import pyautogui, sys
from interface import Interface

class Running:

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    gameName = None
    path = None
    wincap = None
    detector = None
    vision = None
    interface = None
    DEBUG = True
    isRunning = False

    def __init__(self, gameName):
        self.gameName = gameName
        self.interface = 0.7
        self.path = 'assets/warehouse.jpg'
        #get window name
        self.wincap = WindowCapture(self.gameName)

        #load the detector
        self.detector = Detection(self.path)

        #load an empty Vision class
        self.vision = Vision(self.path)


    def close_window(self):
        self.wincap.stop()
        self.detector.stop()
        cv.destroyWindow


    def runstuff(self):
        self.isRunning=True
        self.wincap.start()
        self.detector.start()

        loop_time = time()
        while(True):
        
            #no screenshot? dont run
            if self.wincap.screenshot is None:
                continue

            #give detector current screenshot and threshold
            self.detector.update(self.wincap.screenshot)
            #self.detector.update_threshold(self.interface.get_threshold_from_bar())
            #wincap.update()

            if self.DEBUG:
                #draw detection results onto the original image
                detection_img = self.vision.draw_rectangles(self.wincap.screenshot, self.detector.rectangles)
                #display the images
                cv.imshow(self.gameName, detection_img) 
                #debug the loop rate        
                #print('FPS {}'.format(1/(time()- loop_time)))
                loop_time = time()
                #print (detector.rectangles)
                #WindowCapture.show_cursor_position()

            key = cv.waitKey(1)
            if key == ord('q'):
                self.wincap.stop()
                self.detector.stop()
                cv.destroyAllWindows
                break
            elif key == ord('f'):
                cv.imwrite('positive/{}.jpg'.format(loop_time), self.wincap.screenshot)
            elif key == ord('d'):
                cv.imwrite('negative/{}.jpg'.format(loop_time), self.wincap.screenshot)


        print('Done')




