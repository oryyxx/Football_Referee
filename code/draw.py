import cv2

font = cv2.FONT_HERSHEY_COMPLEX_SMALL
fontScale = 1

def rect(image, text, x1, y1, x2, y2, c):
    global font
    global fontScale

    height, weidth, channels = image.shape

    color = { 0: (255, 0, 0), 1: (0, 255, 0), 2: (0, 0, 255)}

    newImage = cv2.rectangle(image, (x1, y1), (x2, y2), color.get(c, ((0,0,0))), 1)

    if not text == "-1":
        newImage = cv2.putText(image, text, (x1, y1), font, fontScale, 
                 color.get(c, ((0,0,0))), 1, cv2.LINE_AA, False)

    return newImage

def fps(image, fps):
    return cv2.putText(image, ("FPS: " + str(fps)), (0, 16), font, fontScale, 
                 (0,255,0), 1, cv2.LINE_AA, False)
