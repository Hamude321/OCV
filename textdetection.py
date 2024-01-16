import cv2 as cv
from threading import Thread, Lock
from vision import Vision
from time import time
import easyocr


class Textdetection:

    # threading properties
    stopped = True
    lock = None
    rectangles = []
    # properties
    screenshot = None
    loop_time = time()
    fps = 0

    def __init__(self):
        # create a thread lock object
        self.lock = Lock()
        # load the trained model

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def get_detection_fps(self):
        return self.fps
    
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True
    
    def run(self):
        if self.stopped:
            return
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            if not self.screenshot is None:
                #debug time
                # do object detection


                # lock the thread while updating the results
                self.lock.acquire()
                if (time()- self.loop_time)>0:
                    self.fps = int((1/(time()- self.loop_time)))
                    self.loop_time = time()
                self.lock.release()