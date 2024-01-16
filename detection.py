import cv2 as cv
from threading import Thread, Lock
from vision import Vision
from time import time, sleep


class Detection:

    # threading properties
    stopped = True
    lock = None
    rectangles = []
    # properties
    screenshot = None
    threshold = 0.7
    vision = None
    loop_time = time()
    fps = 0

    def __init__(self, vision):
        # create a thread lock object
        self.lock = Lock()
        # load the trained model
        self.vision = vision

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def update_threshold(self, threshold):
        self.lock.acquire()
        self.threshold = threshold
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
                #limit amount of loops
                sleep(1./25)
                #debug time
                # do object detection
                rectangles = self.vision.find(self.screenshot,self.threshold)
                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                if (time()- self.loop_time)>0:
                    self.fps = int((1/(time()- self.loop_time)))
                    self.loop_time = time()
                self.lock.release()