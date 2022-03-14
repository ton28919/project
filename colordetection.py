import cv2
import numpy as np 

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#cred = credentials.Certificate('./test-6dfb1-firebase-adminsdk-kwofl-5341b2b870.json')
cred = credentials.Certificate('./smartfarm-148-firebase-adminsdk-kyij8-18fe509d2e.json')

firebase_admin.initialize_app(cred, {
    #'databaseURL': 'https://test-6dfb1.firebaseio.com/'
    'databaseURL': 'https://smartfarm-148.firebaseio.com/'
})

ref = db.reference('marigold/Growth')

face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
#face_cascade = cv2.CascadeClassifier('./cascade.xml')


cap = cv2.VideoCapture(0)
state = 0
i = 0

#ระยะออกดอก
while i <= 100:
    #Colordetection
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Yellow
    low_yellow = np.array([20, 100, 100])
    high_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
    #yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(yellow_mask, kernel)


    #if yellow == True:
        # Contours detection
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()
        y = approx.ravel()
        #count = count+1

        if area > 400:
            cv2.drawContours(frame, [approx], 0, (0,0,0), 5)

            if len(approx) < 20:
               # print("state 3")
                state = 1
              #  print("state = ",state)
                break
            if len(approx) == 4:
                print("It's a rectangle")

        if state == 1:
            jamekuy = 'ระยะดอก'        


    cv2.imshow("Frame", frame)
    cv2.imshow("Yellow", mask)
    #print(" ",state)
    i += 1


    key = cv2.waitKey(1)
    if key == 27:
        break
#print(i)
ref.set({
    'phase': state
})

#ระยะแรก
j = 0
if state != 1:
    while j <= 100:
        _, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            state = 2

        cv2.imshow('img', img)
        j += 1

        if state == 2:
            jamekuy = 'ระยะต้นกล้า'

        if state == 0:
            jamekuy = 'ไม่มีต้นดาวเรือง'

        k = cv2.waitKey(1)
        if k == 27:
            break

    cap.release

ref.set({
    'phase': jamekuy
})


