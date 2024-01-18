import cv2 as cv
import numpy as np
import os
from detection import Detection
from time import time, sleep, perf_counter
from windowcapture import WindowCapture
from vision import Vision
import pyautogui, sys
from automation import Automation
from horsemarketmanager import HorseMarketManager

class Running:

    
    current_path = os.path.dirname(os.path.abspath(__file__))

    gameName = None
    img_path = None
    wincap = None
    detector = None
    vision = None
    DEBUG = True
    isRunning = False
    screen = None
    detection_img = None
    _return = False
    stop_thread = False
    loop_time = time()
    horsemarketmanager = None
    #automation = None

    needle_images = []

    def __init__(self, gameName, recorded_coords):
        self.gameName = gameName
        self.img_path = 'assets\pics\leaf4.jpg'
        self.img_path = self.current_path+'\\'+self.img_path
        #get window name
        self.wincap = WindowCapture(self.gameName, recorded_coords)

        #load an empty Vision class
        self.vision = Vision(self.img_path)

        #load the detector
        self.detector = Detection(self.vision)

        self.horsemarketmanager = HorseMarketManager()

        #load the automation
        #self.automation = Automation(self.detector)

    def add_additional_needleimage():
        return

    def close_window(self):
        self.wincap.stop()
        self.detector.stop()
        self.horsemarketmanager.stop()
        #self.automation.stop()
        self.stop_thread = True
        return

    def get_detection_img(self):
        return self.detection_img
    
    def get_core_fps(self):
        return self.fps
    
    def runstuff(self):
        self.isRunning=True
        self.wincap.start()
        self.detector.start()
        #self.horsemarketmanager.start()
        # self.automation.start()
      
        
        while(True):
            if self.stop_thread:
                break
        
            #no screenshot? dont run
            if self.wincap.screenshot is None:
                continue

            #give detector current screenshot
            self.detector.update(self.wincap.screenshot)

            self.horsemarketmanager.update(self.wincap.screenshot)


            #draw detection results onto the original image
            self.detection_img = self.vision.draw_rectangles(self.wincap.screenshot, self.detector.rectangles)            

            if self.DEBUG:
                #display the images
                #self.screen = cv.imshow(self.gameName+'1', self.detection_img) 
                #debug the loop rate        
                self.fps=int((1/(time()- self.loop_time)))
                self.loop_time = time()
                # if len(self.detector.rectangles) > 0:
                    # print (self.detector.rectangles)
                #WindowCapture.show_cursor_position()
                # blub = cv.cvtColor(self.detection_img, cv.COLOR_BGR2GRAY)
                # blub = cv.threshold(blub,0,255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
                # cv.imshow('bla',blub )
                #limit amount of loops
                sleep(1./70)

            if self._return:
                sys.exit()

            key = cv.waitKey(1)
            # if key == ord('q'):
            #     self.wincap.stop()
            #     self.detector.stop()
            #     cv.destroyAllWindows
            #     break
            # elif key == ord('f'):
            #     cv.imwrite('positive/{}.jpg'.format(loop_time), self.wincap.screenshot)
            # elif key == ord('d'):
            #     cv.imwrite('negative/{}.jpg'.format(loop_time), self.wincap.screenshot)


        print('Done')




