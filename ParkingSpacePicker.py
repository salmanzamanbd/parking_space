
import cv2
import pickle                                       #this pickle package  we will  use to save all the places and positions  of parking spaces and then we will bring that in our main code """

img = cv2.imread('Carparking.png')


width,height = 30,60                                            # size of the  box

try:                                                 # here it will check that is there any data is in the  pickle file or  not if there is  data it will show picture  with the privious data
    with open('CarParkpos', 'rb') as f:
        posList = pickle.load(f)

except:                                              # if it doesnt find  any  data it will create  a new position list
    posList=[]



def mouseclick( events, x, y, flags, para):
    if events == cv2.EVENT_LBUTTONDOWN:                        #যদি বাম বাটনে ক্লিক পড়ে তাইলে যে এভেন্ট ঘটবে
        posList.append((x,y))                                # উক্ত ইভেন্ট এর ঘটনা স্বরূপ  এক্স এবং ইয়াই এর বক্স তৈরি হবে
    if events == cv2.EVENT_RBUTTONDOWN:                      #for delete the sudden click of left click box
        for i, pos in enumerate(posList):                     #checking where the wight button will click is that in the box or not
            x1,y1 =pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
    with open('CarParkpos','wb' ) as f:                         # After creating or delting  box it will save  that data  in  pickle file
        pickle.dump(posList,f)


while True:
    img = cv2.imread('Carparking.png')                                                  #for relode image
    for pos in posList:                                                                 #বাম বাটনে ক্লিক এ যে বক্স হবে  তার সম্পপরকে তথ্য
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 255), 1)

    cv2.imshow("image", img)
    cv2.setMouseCallback("image",mouseclick)                 #detect mouse click
    cv2.waitKey(1)


