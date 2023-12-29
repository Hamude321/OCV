import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
from cascadeutils import generate_negative_description_file


#workind directory of the folder this is in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture('Legends of Idleon')
#WindowCapture.list_window_names()
cascade_needle = cv.CascadeClassifier('cascade/cascade.xml')
vision_needle = Vision(None)



loop_time = time()
while(True):

    screenshot = wincap.get_screenshot()

    rectangles = cascade_needle.detectMultiScale(screenshot)

    detection_img = vision_needle.draw_rectangles(screenshot, rectangles)

    cv.imshow('Computer Vision', detection_img)
    #cv.imshow('Matches', output_image)

    print('FPS {}'.format(1/(time()- loop_time)))
    loop_time = time()

    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), screenshot)

generate_negative_description_file()
print('Done')






