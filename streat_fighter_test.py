#opencv-python , cvzone, mediapipe
from cvzone.PoseModule import PoseDetector
import cv2
import time
import random as rd
from pygame import mixer

# Starting the mixer
mixer.init()

# Loading the song
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
detector = PoseDetector()
Ryu_Score = 10
Ali_Score = 10

fighter = [
    cv2.imread('img/ryu/ryu2.gif'),
    cv2.imread('img/ryu/ryu2.gif'),
    cv2.imread('img/ryu/ryu3.gif'),
    cv2.imread('img/ryu/ryu4.gif'),
    cv2.imread('img/ryu/ryu5.gif'),
    cv2.imread('img/ryu/ryu6.gif')
]
ryu_fire = cv2.imread('img/ryu/r_fire.png')
#logo = cv2.resize(logo, (390, 803))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output3.avi', fourcc, 20.0, (1800,  1000))

findex = 0
is_Fire = False
x_Fire = 400
while True:

    success, img = cap.read()

    img = cv2.flip(img,1)
    img = cv2.resize(img, (1800, 1000))

    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)
    cv2.putText(img, 'Ryu: ' + str(Ryu_Score), (10, 70), font, 2, (0, 0, 255), 5)
    cv2.putText(img, 'Ali: ' + str(Ali_Score), (1570, 70), font, 2, (255, 0, 0), 5)

    if bboxInfo:
    #if True:
        #mixer.music.load('img/ryu/sf.mp3')
        #mixer.music.set_volume(0.7)
        #mixer.music.play()

        center = bboxInfo["center"]
        if is_Fire:
            cv2.circle(img, (x_Fire - 5, 600), 53, (0, 0, 255), -1)
            cv2.circle(img,(x_Fire,600),50,(250,50,50),-1)

            #print(x_Fire, lmList[1])
            if (x_Fire >= lmList[1][1]-50 and x_Fire <= lmList[1][1] + 100 and lmList[1][2] < 700):
                mixer.music.load('img/ryu/punch.mp3')
                mixer.music.set_volume(0.9)
                mixer.music.play()
                x_Fire = 400
                is_Fire = False
                Ali_Score-=1

            if \
                    (
                    (lmList[19][1] >= 10 and lmList[19][1] <= 250 )
                        or
                    (lmList[20][1] >= 10 and lmList[20][1] <= 250 )
                    ):

                mixer.music.load('img/ryu/punch.mp3')
                mixer.music.set_volume(0.9)
                mixer.music.play()
                Ryu_Score -= 1

            x_Fire += 50
            if (x_Fire > 1800):
                x_Fire = 400
                is_Fire = False

        if not is_Fire:
            i = rd.randint(0, 10)

        if (i == 5):
            print('Fire')
            is_Fire = True
            roi = img[550:950, 0:500]
            ryu_fire = cv2.resize(ryu_fire, (500, 400))
            roi += ryu_fire
            i = -1

        else:
            roi = img[350:950, 0:250]
            fighter[findex] = cv2.resize(fighter[findex], (250, 600))
            roi += fighter[findex]
            findex += 1
            if (findex > 5):
                findex = 0



        time.sleep(0.02)
        #print('Hello')

    cv2.imshow("Image", img)
    if (x_Fire == 450 and i ==-1):
        time.sleep(0.1)
        mixer.music.load('img/ryu/abokin.mp3')
        mixer.music.set_volume(0.9)
        mixer.music.play()

    out.write(img)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()