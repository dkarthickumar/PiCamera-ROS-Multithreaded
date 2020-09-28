#!/bin/env python
#
# Script to detect motion in the frame 
#
import picam_pub as picam
import cv2
import sys
import numpy as np

class motion_detection():
    def __init__(self):
	self.vs = picam.PiVideoStream(frame_size=(320,240), resolution=(1280, 720), framerate=20, ROS=True).start()
	self.fgbg = cv2.createBackgroundSubtractorMOG2()	


    def motion_detect(self):
	while True:
	    try:
	    	frame = self.vs.read()
	     	fgmask = self.fgbg.apply(frame)
		frame = cv2.bitwise_and(frame, frame, mask = fgmask) 
		_, contours,hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	        # Find the index of the largest contour
	        areas = [cv2.contourArea(c) for c in contours]
		if not areas:
		    continue   	
		max_index = np.argmax(areas)
	        cnt=contours[max_index]

	        x,y,w,h = cv2.boundingRect(cnt)
	        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

	    	self.vs.pub_image(frame)
	    except KeyboardInterrupt:
    		print('interrupted!')
		self.vs.stop()
		sys.exit() 
	
if __name__ == '__main__' : 
 	mot = motion_detection()
	mot.motion_detect()		
