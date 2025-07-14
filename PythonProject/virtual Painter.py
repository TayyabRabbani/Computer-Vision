import cv2
import mediapipe as mp
import hand_tracking_module as htm
import numpy as np
import os
import time

brushThickness = 6
eraserThickness = 30

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
folder = "images"
myList = os.listdir(folder)
overlay=[]
detector = htm.HandDetector()

xp=0
yp=0
imgCanvas  = np.zeros((720, 1280, 3), np.uint8) #unsigned 8 bits to it has values from 0-255
ptime = 0

for i in myList:
    image = cv2.imread(os.path.join(folder, i))
    overlay.append(image)

header = overlay[0]
print(len(overlay))
drawColor = (125,120,180)
while True:

    ret, img = cap.read()
    img = cv2.flip(img, 1)

    #Find Landmarks
    img = detector.findHands(img,draw=False)
    lmList = detector.findlength(img,draw=False)
    if (lmList):

        #tips of the index
        x1,y1 = lmList[8][1:]
        #print(x1)

        #check Finger is UP:
        fingers_up = detector.fingersUp()

      # if selection mode -Two finger is up
        if fingers_up[1] and fingers_up[2]:
            xp = 0
            yp = 0
            print("selection")
            #checking clickinf area
            if y1<125:
                if 280<x1<350:
                    header = overlay[0]
                    drawColor = (125,120,180)
                if 590<x1<650:
                    header = overlay[1]
                    print("blue")
                    drawColor = (255,0,0)
                if 890<x1<950:
                    header = overlay[2]
                    print("green")
                    drawColor = (0, 255, 0)
                if 1100<x1<1200:
                    header = overlay[3]
                    print("eraser")
                    drawColor = (0, 0, 0)

        #drawing mode index finger is up
        if fingers_up[1] and fingers_up[2]==0:
            cv2.circle(img,(x1,y1),10,drawColor,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor == (225,225,225):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)

            xp,yp=x1,y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _,imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime

    img[0:125 , 0:1280]= header
    cv2.putText(img, str((int(fps))),(10,70),cv2.FONT_HERSHEY_COMPLEX,1, (255,255,255),1)
    cv2.imshow('Video', img)
    cv2.waitKey(1)