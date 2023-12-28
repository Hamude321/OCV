import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import findClickPositions


#workind directory of the folder this is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture('Legends of Idleon')
#WindowCapture.list_window_names()

loop_time = time()
while(True):

    screenshot = wincap.get_screenshot()

    #cv.imshow('Computer Vision', screenshot)
    findClickPositions('cabbage.png', screenshot, 0.5, 'rectangles')

    print('FPS {}'.format(1/(time()- loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows
        break


print('Done')