import cv2
from cvzone.HandTrackingModule import HandDetector 
from time import sleep
import numpy as np
from cvzone import cornerRect
from pynput.keyboard import Controller
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=1)
finalText=''
keyboard=Controller()
class Button():
    def __init__(self,pos,text,size=(85,85)):
        self.pos=pos
        self.size=size
        self.text=text

buttonList=[]
a=['Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L',';','Z','X','C','V','B','N','M',',','.','/',' ']
for x in range(0,10):
    buttonList.append(Button([100*x+50,100],a[x]))
for x in range(0,10):
    buttonList.append(Button([100*x+50,200],a[x+10]))
for x in range(0,10):
        buttonList.append(Button([100*x+50,300],a[x+20]))
buttonList.append(Button([50,0],a[-1],size=(985,85)))

def drawmore(button,img):
    x,y=button.pos
    w,h=button.size
    # imgNew=np.zeros_like(img,np.uint8)
    cornerRect(img,(button.pos[0],button.pos[1],button.size[0],button.size[1]),20,rt=0)
    cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
    cv2.putText(img,button.text,(x+20,y+60),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img

while True:
    _,img=cap.read()
    img=cv2.flip(img,1)
    img=detector.findHands(img)
    lmList,bboxInfo=detector.findPosition(img,draw=False)
    for x in buttonList:
         img=drawmore(x,img)
    
    if lmList:
         for button in buttonList:
              x,y = button.pos
              w,h = button.size
              if x< lmList[8][0]< x+w and y< lmList[8][1]< y+h:
                 cv2.rectangle(img,(x-7,y-7),(x+w+7,y+h+7),(175,0,175),cv2.FILLED)
                 cv2.putText(img,button.text,(x+20,y+60),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                 l,_,_=detector.findDistance(8,12,img,draw=False)
                #  print(l)
                 if l<40:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x+20,y+60),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    finalText+=button.text
                    keyboard.press(button.text)
                    sleep(0.2)
    cv2.rectangle(img,[50,450],[1000,510],(175,0,175),cv2.FILLED)
    cv2.putText(img,finalText,[60,500],cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)                 
    cv2.imshow('Keyboard',img)
    cv2.waitKey(1)
