import cv2
import pickle
import cvzone
import numpy as np


#video
cap =cv2.VideoCapture('carpark.mp4')                                      #video imported



with open('CarParkpos', 'rb') as f:                                  #  here  it will show the saved  car position in video,  with  boxes
    posList = pickle.load(f)

width,height = 30,60                                                # the box size

def checkParkingSpace(imgProc):
    spaceCounter=0
    #spaceboocked=0                                                  # this function  is for  checking  car parking position
                                                                    # in here  also created loops for croping the image which is being get from the  rectangle
    for pos in posList:


        x,y =pos

        imgCrop =imgProc[y:y+height,x:x+width]
                                                                                                                #cv2.imshow(str(x*y),imgCrop)                                    #str x*y is  creating  random  value for  every image  so that it can show  all image togather
        count = cv2.countNonZero(imgCrop)                                                                       #pixel counter  for  image
        cvzone.putTextRect(img,str(count),(x,y+height-50),scale=0.75,thickness=1,offset=0,colorR=(0,0,255))
        #here pixel less than 260 will be coloured as green  and more than 260  will be shown as red green means empty and red means full
        if count< 230:
            color = (0,255,0)
            thickness=2
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 0), 2)
            cvzone.putTextRect(img, str(count), (x, y + height - 50), scale=0.75, thickness=1, offset=0,
                               colorR=(0, 255, 0))
            spaceCounter = spaceCounter+1
            #cvzone.putTextRect(img, str(spaceCounter), (30, 10), scale=5, thickness=2, offset=5,
                               #colorR=(0, 255, 0))

        else:
            color = (0, 0, 255)
            thickness = 1
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 0, 255), 1)
            cvzone.putTextRect(img, str(count), (x, y + height - 50), scale=0.75, thickness=1, offset=0,
                               colorR=(0, 0, 255))
            #spaceboocked = spaceboocked + 1
            #cvzone.putTextRect(img, f'Parking lot Space counter project with image processing ', (70, 25), scale=2,thickness=1,offset=1, )



    cvzone.putTextRect(img, f'Free Space: {spaceCounter}/{len(posList)}', (50, 25), scale=1, thickness=1, offset=3,                                 #free space  text

                               colorR=(0, 255, 0))


while True:



    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):              # here "CAP_PROP_POS_FRAMES"It will give us the current frame of the video
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)                              # here  the frames are being  reseting when it reach the  total amount of frames    ultimatly it is making a loop                             # "CAP_PROP_FRAME_COUNT" it will show us the  total frame of the video

    success, img = cap.read()
    # for knowing  is there  any car or not on that  region , we have to look in its pixel count if there  is pixel  there is car but there   is no pixel there is no car . for that we need to convert the image into binary image

    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                       # for thresholding   the image will be converted in to gray scale
    imgBlur =cv2.GaussianBlur(imgGray,(5,5),2)
    imgThreshold =cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)             #converting into binary image
    imgMedian =cv2.medianBlur(imgThreshold,5)                                                                                    # to remove soft dots/ pixels
    kernel= np.ones((3,3),np.uint8)

    imgDilate =cv2.dilate(imgMedian,kernel,iterations=1)                                                                    # it will make the  pixel thick which will  help to differentiate  between empty space and full space

    checkParkingSpace(imgDilate)
    #for pos in posList:
        #cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 255), 1)

    cv2.imshow("image",img)
    # cv2.imshow("imageBlur", imgBlur)
    #cv2.imshow("imageThres", imgMedian)
    cv2.waitKey(200)
