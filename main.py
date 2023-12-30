import cv2 as cv
import numpy as np
import os
from detection import Detection
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
from cascadeutils import generate_negative_description_file
from bot import GameBot,BotState


#workind directory of the folder this is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

wincap = WindowCapture('Legends of Idleon')
#WindowCapture.list_window_names()

#load the detector
detector = Detection('cascade/cascade.xml')

#load an empty Vision class
vision = Vision()

# initialize the bot
bot = GameBot((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h))

wincap.start()
detector.start()
bot.start()

loop_time = time()
while(True):

    #no screenshot? dont run
    if wincap.screenshot is None:
        continue

    #give detector current screenshot
    detector.update(wincap.screenshot)

    # # update the bot with the data it needs right now
    # if bot.state == BotState.INITIALIZING:
    #     # while bot is waiting to start, go ahead and start giving it some targets to work
    #     # on right away when it does start
    #     targets = vision.get_click_points(detector.rectangles)
    #     bot.update_targets(targets)
    # elif bot.state == BotState.SEARCHING:
    #     # when searching for something to click on next, the bot needs to know what the click
    #     # points are for the current detection results. it also needs an updated screenshot
    #     # to verify the hover tooltip once it has moved the mouse to that position
    #     targets = vision.get_click_points(detector.rectangles)
    #     bot.update_targets(targets)
    #     bot.update_screenshot(wincap.screenshot)
    # elif bot.state == BotState.MOVING:
    #     # when moving, we need fresh screenshots to determine when we've stopped moving
    #     bot.update_screenshot(wincap.screenshot)
    # elif bot.state == BotState.MINING:
    #     # nothing is needed while we wait for the mining to finish
    #     pass

    if DEBUG:
        #draw detection results onto the original image
        detection_img = vision.draw_rectangles(wincap.screenshot, detector.rectangles)
        #display the images
        cv.imshow('Computer Vision', detection_img) 
        #debug the loop rate
        #print('FPS {}'.format(1/(time()- loop_time)))
        print(detector.rectangles)
        loop_time = time()

    key = cv.waitKey(1)
    if key == ord('q'):
        wincap.stop()
        detector.stop()
        bot.stop()
        cv.destroyAllWindows
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), wincap.screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), wincap.screenshot)

generate_negative_description_file()
print('Done')






