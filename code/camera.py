from PIL import Image
import cv2

#Set the camera to the primary camera of hardware
cap = cv2.VideoCapture(0)

#Variable for storing the image
Image = None

#------------------- IMPORTANT ---------------------
# IF YOU WANT TO PROCCESS AN IMAGE SIMPLY FOLLOW THE EXAMPLE BELOW
# 
# EXAMPLE:
# import camera
# image = camera.getImage() 
def getImage():
    return Image

#Capture the image (DONT USE THIS)
def updateImage():
    global Image

    ret, frame = cap.read()
    if ret:

        rawImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        Image = cv2.flip(rawImage, 1)
    else:
        print("ERROR: NOT ABLE TO RETRIVE VIDEO DATA...")

#not being used
def closeCamera():
    cap.release()