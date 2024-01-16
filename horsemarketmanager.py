import easyocr
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from threading import Thread, Lock
from time import time, sleep

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
        self.reader = easyocr.Reader(['en'], gpu=False)
    
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
        # img = cv.imread(img)

        # detect text on image
        text_ = self.reader.readtext(img)

        for t in text_:
            _, text, _ = t
            if any(x in text for x in self.matches):
                splits = text.split(' ')
                tier = splits[0] + ' ' + splits[1]
                silver = splits[2]
                registration = (splits[-1].replace(')','')).replace('(','')

                #add entry
                entry = self.HorseMarketEntry(tier, silver, registration)

                if not entries is None:
                    if not any(entry == existing_entry for existing_entry in entries):
                        entries.append(entry)
        return entries

    # for e in entries:
    #     print(e.tier+' '+e.silver+' '+str(e.registration))
    # print(entries)
    # print(len(entries))

    # plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    # plt.show()

    def run(self):
        if self.stopped:
            return
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            if not self.screenshot is None:
                sleep(1)
                #debug time
                # do object detection
                entries = self.add_entry(self.entries, self.screenshot)
                if not self.entries is None:
                    print(len(self.entries))
                # lock the thread while updating the results
                self.lock.acquire()
                self.entries = entries
                self.lock.release()  

# manager = HorseMarketManager()
# manager.add_entry(HorseMarketManager.image_path)
# manager.add_entry('assets\pics\\bdochat.jpg')
# manager.add_entry(HorseMarketManager.image_path)

# print(len(manager.entries))
# print(manager.entries[0].silver)
