import os
import cv2
from cvzone.HandTrackingModule import HandDetector

#varables
width, height = 1280, 1024
folderpath = "presentation"
click = False
counter = 0
delay = 35


#camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

#geting the list of presentation images
pathimages = sorted(os.listdir(folderpath), key=len)


#variable
imagenumber = 0
hs, ws = int(120*1), int(213*1)
gesthreshold = 400

#detector
ditector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathfullimage = os.path.join(folderpath, pathimages[imagenumber])
    imagecurrent = cv2.imread(pathfullimage)

    hands, img = ditector.findHands(img)
    cv2.line(img,(0, gesthreshold), (width, gesthreshold), (10, 255, 0),5 )

    if hands and click is False:
        hand = hands[0]
        fingers = ditector.fingersUp(hand)
        cx, cy = hand['center']
        # print(fingers)

        if cy <=gesthreshold:

            #gesture 1 - left
            if fingers == [1, 0, 0, 0, 0]:
                print('left')
                if imagenumber > 0:
                    click = True
                    imagenumber -= 1

            # gesture 2 - right
            if fingers == [0, 1, 1, 0, 0]:
                print('right')
                if imagenumber < len(pathimages)-1:
                    click = True
                    imagenumber += 1

#click iteration
    if click:
        counter += 1
        if counter > delay:
            counter = 0
            click = False

    #adding webcam
    imgsmall = cv2.resize(img, (ws, hs))
    h, w, _ = imagecurrent.shape
    imagecurrent[0:hs, w-ws:w] = imgsmall


    cv2.imshow("image", img)
    cv2.imshow("slides", imagecurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
