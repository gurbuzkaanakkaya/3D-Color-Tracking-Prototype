import cv2
import numpy as np
from collections import deque
import serial
import struct 
import time

seri = serial.Serial("COM6",9600)   
time.sleep(2)

buffer_size = 16
pts = deque(maxlen = buffer_size)

#blue low-up
blueLower =(84,98,0)
blueUpper =(179,255,255)
list_box =[4]

#capture
cap = cv2.VideoCapture(0)

xlis=[90] 
ylis=[90] 
success, img = cap.read()

def servo(center_x,center_y):     
    if center_x < 300 and center_x > 340:
        print("kilitlendi_x")
        xlis.append(xlis[len(xlis)-1])  
        xlis.remove(xlis[0]) 

    elif center_x > 340: 
        print("sag")
        xlis.append(xlis[len(xlis)-1]-1) 
        xlis.remove(xlis[0])    
        

    elif center_x < 300: 
        print("sol")
        xlis.append(xlis[len(xlis)-1]+1) 
        xlis.remove(xlis[0])

    xdeg=xlis[len(xlis)-1] 
    
    
    if center_y < 220 and center_y > 260:
        print("kilitlendi_y")
        ylis.append(ylis[len(ylis)-1])
        ylis.remove(ylis[0])

    elif center_y > 260:
        print("yukari")
        ylis.append(ylis[len(ylis)-1]+1)
        ylis.remove(ylis[0])

    elif center_y < 220:
        print("asagi")
        ylis.append(ylis[len(ylis)-1]-1)
        ylis.remove(ylis[0])

    ydeg=ylis[len(ylis)-1]
    
    
    if xdeg >= 180:
        xlis.append(xlis[len(xlis)-1]-1)
        xlis.remove(xlis[0])
        print("x ekseni sınır acısı 180 derece")
    elif xdeg <= 0:
        xlis.append(xlis[len(xlis)-1]+1)
        xlis.remove(xlis[0])
        print("x ekseni sınır acısı 0 derece")
    if ydeg >= 180:
        ylis.append(ylis[len(ylis)-1]-1)
        ylis.remove(ylis[0])
        print("y ekseni sınır acısı 180 derece")
    elif ydeg <= 0:
        ylis.append(ylis[len(ylis)-1]+1)
        ylis.remove(ylis[0])
        print("y ekseni sınır acısı 0 derece")
    
        
    seri.write(struct.pack('>BB', xdeg,ydeg))

while True:
    success,imgOriginal  = cap.read()
    timer = cv2.getTickCount()
    success, img = cap.read()
   
    
    if success:
        #blur
        blurred = cv2.GaussianBlur(imgOriginal,(11,11), 0)
        
        #hsv
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)     
               
        #mask
        mask = cv2.inRange(hsv,blueLower,blueUpper)
        mask = cv2.erode(mask, None , iterations = 2)
        mask = cv2.dilate(mask, None , iterations = 2)
      
        #contour
        contours, hierarchy= cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)        
        center = None
        
        
        if len(contours) > 0:           
            c = max(contours,key = cv2.contourArea)            
           
            rect = cv2.minAreaRect(c)           
            ((x,y),(width,height),(rotation)) = rect         
            print(" ")
           
            s = "x:{}, y:{}, width{}, height:{}, rotation:{}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
            print(s)
            center_x = int(x+width/2)
            center_y = int(y+height/2)
            
            #boxes
            box =  cv2.boxPoints(rect)
            box = np.int64(box)
                       
            #moment
            M = cv2.moments(c)
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
                  
            #contour
            cv2.drawContours(imgOriginal, [box], 0,(0,255,255),2)
            
            #center cricle
            cv2.circle(imgOriginal, center , 5 , (255,0,255),-1)
                        
            #putText
            cv2.putText(imgOriginal,s,(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),2)
            servo(center_x,center_y)
        #deque
        pts.appendleft(center)
        
        for i in range(1,len(pts)):
            if pts[i-1] is None or pts[i] is None: continue
            cv2.line(imgOriginal,pts[i-1],pts[i],(0,255,0),3)
        
            
        cv2.imshow("track",imgOriginal)
          
    if cv2.waitKey(1) & 0xFF ==ord("q"): break


