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

gameName = 'Legends of Idleon'
path = 'assets/shroom.jpg'

wincap = WindowCapture(gameName)

#load the detector
detector = Detection(path)

#load an empty Vision class
vision = Vision(path)

WindowCapture.list_window_names()
  
wincap.start()
detector.start()

loop_time = time()
while(True):

    #no screenshot? dont run
    if wincap.screenshot is None:
        continue

    #give detector current screenshot
    detector.update(wincap.screenshot)

    x, y = pyautogui.position()
    positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    print(positionStr, end='')
    print('\b' * len(positionStr), end='', flush=True)

    if DEBUG:
        #draw detection results onto the original image
        detection_img = vision.draw_rectangles(wincap.screenshot, detector.rectangles)
        #display the images
        cv.imshow(gameName, detection_img) 
        #debug the loop rate
        #print('FPS {}'.format(1/(time()- loop_time)))
        loop_time = time()

    key = cv.waitKey(1)
    if key == ord('q'):
        wincap.stop()
        detector.stop()
        cv.destroyAllWindows
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), wincap.screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), wincap.screenshot)

print('Done')




