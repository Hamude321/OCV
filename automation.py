import pyautogui
from time import sleep
import cv2 as cv
from threading import Thread, Lock
from detection import Detection

class Automation:

    # threading properties
    stopped = True
    lock = None 
    # properties
    detector = None 
    i=0

    def __init__(self,detector):
        # create a thread lock object
        self.lock = Lock() 
        self.detector = detector  

    def actions(self, rectangles):
        if(self.i==0):
            sleep(10)
            self.i+=1
        if len(rectangles)>0:
            pyautogui.press('space')
            print('Space')
            sleep(1)  

    # threading methods
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()        
    
    def stop(self):
        self.stopped = True
    
    def run(self):
        while not self.stopped:
            self.actions(self.detector.rectangles)