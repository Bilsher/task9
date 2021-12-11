import cv2
import numpy as np
import time

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera")

lower = (0, 70, 170)
upper = (10, 255, 255)

lower1 = (55, 110, 150)
upper1 = (150, 255, 255)

def test(lower, upper):
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
   #mask = cv2.dilate(mask, None, iterations = 2)
    return mask

def test2(cnts, image, color):
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (curr_x, curr_y), radius = cv2.minEnclosingCircle(c)
        #print(yes)
        if radius > 10:
            cv2.circle(image, (int(curr_x) ,int(curr_y)), int(radius),
                                (0,255, 255),2)
            
   # if len(cnts1) > 0:
    #    c = max(cnts1, key=cv2.contourArea)
     #   (curr_x, curr_y), radius = cv2.minEnclosingCircle(c)
      #  if radius > 10:
       #     cv2.circle(image, (int(curr_x) ,int(curr_y)), 5,
      
          
          
while cam.isOpened():
    _, image = cam.read()
    blurred = cv2.GaussianBlur(image, (11,11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    mask = test(lower, upper)
    mask1 = test(lower1, upper1)
    sumask = mask1 + mask 
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    test2(cnts, image, (0,0,255))
    test2(cnts1, image, (255,0,0))
    
    
    
    cv2.imshow("Camera", image)
    cv2.imshow("Mask", mask)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
    
cam.release()
cv2.destroyAllWindows()