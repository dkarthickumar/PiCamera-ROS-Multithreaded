#!/bin/env python
#
# Script to detect motion in the frame 
#
import picam_pub as picam
import cv2
import sys

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
		(_, cnts, _) = cv2.findContours(fgmask, cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
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
 	mot = motion_detection()
	mot.motion_detect()		
