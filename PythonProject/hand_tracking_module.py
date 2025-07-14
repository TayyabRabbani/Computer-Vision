import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self,mode=False,MaxHands=1,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.MaxHands = MaxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.MaxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds =[4,8,12,16,20]

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:

                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    def findlength(self,img,handNo=0,draw=False):
        self.lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for idx, lms in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lms.x * w), int(lms.y * h)
                self.lmlist.append([idx, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        return self.lmlist

    def fingersUp(self): #its flipped
        if not hasattr(self, 'lmlist') or len(self.lmlist) != 21:
            return []


        fingers = []

        # Thumb
        if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # four fingers
        for i in range(1, len(self.tipIds)):
            if self.lmlist[self.tipIds[i]][2] < self.lmlist[self.tipIds[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

def main():
    ptime = 0
    detector = HandDetector()

    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        cTime = time.time()
        fps = 1 / (cTime - ptime)
        ptime = cTime

        lmlist = detector.findlength(img,draw=False)
        if len(lmlist) > 0:
            print(lmlist[4])
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 255), 3)
        cv2.imshow('Video', img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()