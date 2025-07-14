import cv2
import time
import os
import hand_tracking_module as htm

wCam, hCam = 640, 480

cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
ptime=0

tipIds=[4,8,12,16,20]

detector=htm.HandDetector(MaxHands=2)
while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findlength(img,handNo=0)
    if lmlist:
        fingers=[]

        #Thumb
        if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #four fingers
        for i in range(1,len(tipIds)):
            if lmlist[tipIds[i]][2] < lmlist[tipIds[i]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers= fingers.count(1)
        print(total_fingers)


    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (10, 70), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(255, 255, 255),
                thickness=2)
    cv2.imshow('Video', img)
    cv2.waitKey(1)