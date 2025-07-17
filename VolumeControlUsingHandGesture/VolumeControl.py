import cv2
import time
import numpy as np
import mediapipe as mp
import hand_tracking_module as htm
import math
from ctypes import cast, POINTER
from comtypes  import  CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,None)
volume = cast(interface,POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=(volume.GetVolumeRange())
#(-63.5, 0.0, 0.5)
minVol= volRange[0]
maxVol= volRange[1]
smoothVol = 0
alpha = 0.2  # Smoothing factor (0 = very smooth, 1 = no smoothing)


wCam, hCam = 720, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
ptime=0
detector = htm.HandDetector()

while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findlength(img,draw=False)
    if len(lmlist)>0 :
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img,(x1,y1),5,(255,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),5,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),1)
        cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED)

        length = math.hypot(x2-x1,y2-y1)

        #HandRamge 25-200
        #VolRange -63 to 0
        vol = np.interp(length, [25, 160], [minVol, maxVol])
        smoothVol = alpha * vol + (1 - alpha) * smoothVol  # Low-pass filter
        volume.SetMasterVolumeLevel(smoothVol, None)

        volPercent = np.interp(smoothVol, [minVol, maxVol], [0, 100])
        cv2.putText(img, f'{int(volPercent)} %', (40, 450),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)


    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime


    cv2.putText(img,str(int(fps)),(10,70),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=1,color=(255,255,255),thickness=2)
    cv2.imshow('Video', img)
    cv2.waitKey(1)

