import numpy as np
import win32gui, win32ui, win32con
from threading import Thread,Lock

class WindowCapture:

    #threading properties
    stopped = True
    lock = None
    screenshot = None
    #properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, window_name=None):
        #create thread lock object
        self.lock = Lock()

        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None,window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))

        #monitor width and height
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        border_pixels = 8 
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h -titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y
        


    def get_screenshot(self):

        #get the window image data
        hwnd = win32gui.FindWindow(None, 'Legends Of Idleon')

        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0), (self.w, self.h), dcObj, (self.cropped_x,self.cropped_y), win32con.SRCCOPY)

        #save the screenshot
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')

        signedInsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedInsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        #free ressources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]
        img = np.ascontiguousarray(img)

        return img

    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):

        while not self.stopped:
            if not self.screenshot is None:
                #get an updated image of the game
                screenshot = self.get_screenshot()
                #lock the thread while updating the results
                self.lock.acquire()
                self.screenshot = screenshot
                self.lock.release()