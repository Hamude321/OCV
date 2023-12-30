import cv2 as cv
import numpy as np
import os
from detection import Detection
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
import pyautogui, sys

#workind directory of the folder this is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

gameName = 'BLACK DESERT - 458855'
path = 'assets/warehouse.jpg'
threshold = 0.5
detection_img = None

#get window name
wincap = WindowCapture(gameName)

#load the detector
detector = Detection(path, threshold)

#load an empty Vision class
vision = Vision(path)

WindowCapture.list_window_names()
  
wincap.start()
detector.start()
vision.start()

loop_time = time()
while(True):

    #no screenshot? dont run
    if wincap.screenshot is None:
        continue

    #give detector current screenshot
    detector.update(wincap.screenshot)
    vision.update(wincap.screenshot)
    vision.update(detector.rectangles)
    detection_img =vision.detection_img

    if DEBUG:
        #display the images
        if vision.detection_img is None:
            print('rip')
        else:
            cv.imshow(gameName, detection_img) 
        #debug the loop rate        
        #print('FPS {}'.format(1/(time()- loop_time)))
        loop_time = time()
        #print (detector.rectangles)
        WindowCapture.show_cursor_position()

    key = cv.waitKey(1)
    if key == ord('q'):
        wincap.stop()
        detector.stop()
        vision.stop()
        cv.destroyAllWindows
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), wincap.screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), wincap.screenshot)

print('Done')




