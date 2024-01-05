import cv2 as cv
import numpy as np
import os
from detection import Detection
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
import pyautogui, sys


class Running:

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    gameName = None
    path = None
    wincap = None
    detector = None
    vision = None
    DEBUG = True
    isRunning = False
    screen = None
    detection_img = None
    _return = False
    stop_thread = False

    def __init__(self, gameName, x1=0,x2=0,y1=0,y2=0):
        self.gameName = gameName
        self.path = 'assets/leaf4.jpg'
        #get window name
        self.wincap = WindowCapture(self.gameName, x1,x2,y1,y2)

        #load an empty Vision class
        self.vision = Vision(self.path)

        #load the detector
        self.detector = Detection(self.vision)


    def close_window(self):
        self.wincap.stop()
        self.detector.stop()
        self.stop_thread = True
        return

    def get_detection_img(self):
        return self.detection_img

    def runstuff(self):
        self.isRunning=True
        self.wincap.start()
        self.detector.start()

        loop_time = time()
        while(True):
            if self.stop_thread:
                break
        
            #no screenshot? dont run
            if self.wincap.screenshot is None:
                continue

            #give detector current screenshot and threshold
            self.detector.update(self.wincap.screenshot)
            #wincap.update()
            # if(self.vision.max_val>=0.87):
            #     pyautogui.press('space')
            #     print('Space')
            #     self.vision.max_val =0
            #     sleep(0.1)

            if self.DEBUG:
                #draw detection results onto the original image
                detection_img = self.vision.draw_rectangles(self.wincap.screenshot, self.detector.rectangles)
                #display the images
                self.detection_img = detection_img
                self.screen = cv.imshow(self.gameName+'1', detection_img) 
                #debug the loop rate        
                # print('FPS {}'.format(1/(time()- loop_time)))
                # loop_time = time()
                # if len(self.detector.rectangles) > 0:
                    # print (self.detector.rectangles)
                #WindowCapture.show_cursor_position()

            if self._return:
                sys.exit()

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




