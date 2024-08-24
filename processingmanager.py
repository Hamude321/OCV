import easyocr
from threading import Thread, Lock
from time import time, sleep
import cv2 as cv

class ProcessingManager:

    # threading properties
    stopped = True
    lock = None
    screenshot = None

    entries=[]
    reader = None
    entry = None


    def __init__(self):
        self.lock = Lock()
        # instance text detector  
        self.reader = easyocr.Reader(['en'], gpu=True)
    
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

          
    def add_entry(self, img):  
        divider = 0
        max_weight = 0 
        current_weight = 0

        #convert img to grayscale
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #convert img to black and white pixels
        #img = cv.threshold(img, 0,255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
        # detect text on image
        text_ = self.reader.readtext(img)
        print(text_)
        print('-------------------')


        for t in text_:
            _, text, _ = t
            splits = text.split(' ')
            if len(splits)>1:
                current_weights = splits[0].replace(',','')
                current_weights = current_weights.split('.')
                current_weight = int(current_weights[0])

                max_weights = splits[1].replace(',','')
                max_weights = max_weights.split('.')
                max_weight = int(max_weights[0])

                divider = float(max_weight/current_weight)
            else:
                print('Too many splits?:', len(splits))
                
        if divider is not None:
            if divider<1:
                print('Max:',max_weight,'Current:', current_weight, 'Factor:', divider)
                print('Empty Bags')
            else:
                print('Max:',max_weight,'Current:', current_weight, 'Factor:', divider)
                print('Bags have Space')

               

    def run(self):
        if self.stopped:
            return
        while not self.stopped:
            if not self.screenshot is None:
                sleep(5)
                # search img
                self.add_entry(self.screenshot)