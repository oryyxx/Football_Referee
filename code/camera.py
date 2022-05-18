import cv2
from PIL import Image
import os

#Set the camera to the primary camera of hardware
cap = cv2.VideoCapture(0)

#Variable for storing the image
Image = None

#returns the latest image from the camera
def getImage():
    return Image

#Capture the image 
def updateImage():
    global Image

    ret, frame = cap.read()
    if ret:
        ret, frame = cap.read()
        rawImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        Image = cv2.flip(rawImage, 1)
    else:
        print("ERROR: NOT ABLE TO RETRIVE VIDEO DATA...")

#not being used
def closeCamera():
    cap.release()