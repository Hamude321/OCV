import cv2 as cv
from threading import Thread, Lock
from vision import Vision
from time import time


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
                # print('FPS {}'.format(1/(time()- self.loop_time)))
                # self.loop_time = time()
                # do object detection
                rectangles = self.vision.find(self.screenshot,self.threshold)
                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()