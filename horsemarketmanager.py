import easyocr
from threading import Thread, Lock
from time import time, sleep
import cv2 as cv

class HorseMarketManager:
    class HorseMarketEntry:
        def __init__(self, tier, silver, registration):
            self.tier = tier
            self.silver = silver
            self.registration = registration

        def __eq__(self, other):
            if isinstance(other, HorseMarketManager.HorseMarketEntry):
                return (
                    self.tier == other.tier
                    and self.silver == other.silver
                    and self.registration == other.registration
                )
            return False

    # threading properties
    stopped = True
    lock = None
    screenshot = None

    entries=[]
    matches = ["Tier 8", "Dream Horse"]
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
      
    def add_entry(self, entries, img):         

        #convert img to grayscale
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #convert img to black and white pixels
        #img = cv.threshold(img, 0,255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
        # detect text on image
        text_ = self.reader.readtext(img)

        for t in text_:
            _, text, _ = t
            if any(x in text for x in self.matches):
                splits = text.split(' ')
                if len(splits)>4:
                    tier = splits[0] + ' ' + splits[1]
                    silver = splits[2].replace('.',',')
                    registration = ((splits[-1].replace(')','')).replace('(','')).replace('.',':')

                    #add entry
                    entry = self.HorseMarketEntry(tier, silver, registration)

                    #check for duplicates
                    if not entries is None:
                        if not any(entry == existing_entry for existing_entry in entries):
                            entries.append(entry)
        return entries

    def run(self):
        if self.stopped:
            return
        while not self.stopped:
            if not self.screenshot is None:
                sleep(5)
                # search img
                entries = self.add_entry(self.entries, self.screenshot)
                # lock the thread while updating the results
                self.lock.acquire()
                self.entries = entries
                self.lock.release()  

