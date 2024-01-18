import pyautogui
import cv2 as cv
from time import sleep
import random

# pyautogui.displayMousePosition()
# random.randrange(2, 20)

x=True
sleep(2)
#click item
while x==True:
    pyautogui.moveTo(x=random.randrange(164, 500) , y=random.randrange(1017, 1070))
    pyautogui.click()
    sleep(random.randrange(1, 5)/10)
    pyautogui.click()


    #click pen
    sleep(0.5)
    pyautogui.moveTo(x=random.randrange(132, 255), y=random.randrange(1144, 1174))
    sleep(random.randrange(1, 5)/10)
    pyautogui.click()



    key = cv.waitKey(1)
    if key == ord('q'):
        x=False
        sleep(10)