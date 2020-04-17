#!/bin/env python
#
# Script to object tracking in the frame 
#
import picam_pub as picam
import cv2
import sys

class object_tracking():
    def __init__(self):
	self.vs = picam.PiVideoStream(frame_size=(320,240), resolution=(1280, 720), framerate=20, ROS=True).start()

    def track_object(self):
	while True:
	    try:
	    	frame = self.vs.read()
	    	self.vs.pub_image(frame)
	    except KeyboardInterrupt:
    		print('interrupted!')
		self.vs.stop()
		sys.exit() 
	
if __name__ == '__main__' : 
 	obj_trk = object_tracking()
	obj_trk.track_object()		
