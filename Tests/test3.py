import pyautogui
import time
from time import sleep

def hold_W (hold_time):
    import time, pyautogui
    start = time.time()
    while time.time() - start < hold_time:
        pyautogui.press('space')



sleep(2)
start = time.time()                    
while time.time() - start < 2: #Hold Key for 5 Seconds
    pyautogui.press('space')