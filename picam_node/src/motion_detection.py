#!/bin/env python
#
# Script to detect motion in the frame 
#
import picam_pub as picam
import cv2

class motion_detection():
    def __init__(self):
	self.vs = picam.PiVideoStream(frame_size=(320,240), resolution=(1280, 720), framerate=20, ROS=True).start()
	self.fgbg = cv2.createBackgroundSubtractorMOG2()	


    def motion_detect(self):
	while True:
	    try:
	    	frame = self.vs.read()
	     	fgmask = self.fgbg.apply(frame)
	    	self.vs.pub_image(fgmask)
	    except KeyboardInterrupt:
    		print('interrupted!')
		self.vs.stop()
		break 
	
if __name__ == '__main__' : 
 	mot = motion_detection()
	mot.motion_detect()		
