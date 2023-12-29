import cv2 as cv
from threading import Thread, Lock
from vision import Vision

vision = Vision('assets/bear.jpg')

class Detection:

    # threading properties
    stopped = True
    lock = None
    rectangles = []
    # properties
    needle_img_path = None
    screenshot = None
    threshhold = 0.3

    def __init__(self, needle_img_path):
        # create a thread lock object
        self.lock = Lock()
        # load the trained model
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            if not self.screenshot is None:
                # do object detection
                rectangles = vision.find(self.screenshot,self.threshhold)
                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()