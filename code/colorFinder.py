#A simple program that helps in finding a color from a webcam

import cv2
import cvzone
import numpy as np
from cvzone.ColorModule import ColorFinder

colorFinder = ColorFinder(True)

hsv = {'hmin': 9, 'smin': 45, 'vmin': 54, 'hmax': 19, 'smax': 255, 'vmax': 255}


vid = cv2.VideoCapture(0)
  
while(True):
      
    ret, frame = vid.read()

    imageBlur = cv2.GaussianBlur(frame, (7,7), 1)
    imageColor, mask = colorFinder.update(imageBlur, hsv)

    cv2.imshow('frame', imageColor)
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv2.destroyAllWindows()