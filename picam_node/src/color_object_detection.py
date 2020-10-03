#!/bin/env python
#
# Script to object tracking in the frame using color filtering method 
#
import picam_pub as picam
import cv2
import sys
from motor_cmd import motor_ctrl

class color_object_detection():
    def __init__(self):
	self.vs = picam.PiVideoStream(frame_size=(320,240), resolution=(1280, 720), framerate=30, ROS=True).start()
	self.motor = motor_ctrl()


    def detect_object(self,roi_hist):
	while True:
	    try:
	    	frame = self.vs.read()
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
		mask = cv2.calcBackProject([hsv],[0,1],roi_hist,[0,180,0,256],1)
 		(_,cnts, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for c in cnts:
		    if cv2.contourArea(c) < 20:
			continue
		    (x,y,w,h) = cv2.boundingRect(c)
		    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
		    
	    	self.vs.pub_image(frame)
	    except KeyboardInterrupt:
    		print('interrupted!')
		self.vs.stop()
		sys.exit() 

if __name__ == '__main__' : 
 	clr_obj_dect = color_object_detection()
	img = clr_obj_dect.vs.read()
	roi = img[120:130,130:140]
	roi_hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
	roi_hist = cv2.calcHist([roi_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
	clr_obj_dect.detect_object(roi_hist)		
