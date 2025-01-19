import easyocr
from threading import Thread, Lock
from time import time, sleep
import cv2
import matplotlib.pyplot as plt


# read image
image_path = 'assets\pics\pal.jpg'

# img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

img = cv2.imread(image_path)

height, width, channe = img.shape


#img = img[int(height*(4/100)):int(height*(18/100)), int(width*(25/1000)): int(width*(85/1000))]

img = img[int(height*(282/500)) : int(height*(400/500)), int(width*(757/1000)) : int(width*(982/1000))]

# instance text detector
reader = easyocr.Reader(['en'])

# detect text on image
text_ = reader.readtext(img)

threshold = 0.25
# draw bbox and text
for t_, t in enumerate(text_):
    print(t)

    bbox, text, score = t

    if score > threshold:
        cv2.rectangle(img, bbox[0], bbox[2], (0, 255, 0), 5)
        cv2.putText(img, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()
print(img.shape)