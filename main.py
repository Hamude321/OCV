import cv2 as cv
import numpy as np
import os
from detection import Detection
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
from cascadeutils import generate_negative_description_file
import pyautogui
from threading import Thread


#workind directory of the folder this is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture('Legends of Idleon')
#WindowCapture.list_window_names()

#load the detector
detector = Detection('cascade/cascade.xml')

#load an empty Vision class
vision = Vision(None)

is_bot_in_action = False

DEBUG = True

def bot_actions(rectangles):
    #take bot actions
    if len(rectangles) > 0:
        targets = vision.get_click_points(rectangles)
        target = wincap.get_screen_position(targets[0])
        pyautogui.moveTo(x=target[0], y=target[1])
        #pyautogui.click
        sleep(5)
    global is_bot_in_action
    is_bot_in_action = False

wincap.start()
detector.start()

loop_time = time()
while(True):

    if wincap.screenshot is None:
        continue

    #do object detection
    detector.update(wincap.screenshot)

    if DEBUG:
        #draw detection results onto the original image
        detection_img = vision.draw_rectangles(wincap.screenshot, detector.rectangles)
        #display the images
        cv.imshow('Computer Vision', detection_img) 

    if not is_bot_in_action:
        is_bot_in_action=True
        t = Thread(target=bot_actions, args=(detector.rectangles,))
        t.start()

    #debug the loop rate
    print('FPS {}'.format(1/(time()- loop_time)))
    loop_time = time()

    key = cv.waitKey(1)
    if key == ord('q'):
        wincap.stop()
        detector.stop()
        cv.destroyAllWindows
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), screenshot)

generate_negative_description_file()
print('Done')






