#!/bin/env python
#
# Script to object tracking in the frame using color filtering method 
#
import picam_pub as picam
import cv2
import sys
from motor_cmd import motor_ctrl

class object_tracking():
    def __init__(self):
	self.vs = picam.PiVideoStream(frame_size=(320,240), resolution=(1280, 720), framerate=30, ROS=True).start()

    def track_object(self,low_color, high_color):
	while True:
	    try:
	    	frame = self.vs.read()
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
		mask = cv2.inRange(hsv, low_color, high_color)
 		(_,cnts, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for c in cnts:
		    if cv2.contourArea(c) < 20:
			continue
		    (x,y,w,h) = cv2.boundingRect(c)
		    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
		    
		    midx = x + (w/2)
		    midy = y + (h/2)

		    errx = (320/2) - midx
		    erry = (240/2) - midy
		    if errx < 40 and erry < 40:	
			print errx, erry 

	    	self.vs.pub_image(frame)
	    except KeyboardInterrupt:
    		print('interrupted!')
		self.vs.stop()
		sys.exit() 

if __name__ == '__main__' : 
 	obj_trk = object_tracking()
	pink_lower = (92, 89, 6)
	pink_higher = (140, 255, 255)
	obj_trk.track_object(pink_lower, pink_higher)		
