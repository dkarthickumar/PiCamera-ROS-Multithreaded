#!/bin/env python
#
# Script to object tracking in the frame 
#
import picam_pub as picam
import cv2
import sys
from motor_cmd import motor_ctrl

class object_tracking():
    def __init__(self):
	self.vs = picam.PiVideoStream(frame_size=(320,240), resolution=(1280, 720), framerate=30, ROS=True).start()
	self.tracker = cv2.TrackerCSRT_create()
	self.motor = motor_ctrl()

    def track_object(self):
	while True:
	    try:
	    	frame = self.vs.read()
		ok,bbox = self.tracker.update(frame)
        	# Draw bounding box
	        if ok:
            	    # Tracking success
             	    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                    midx = (int(bbox[0] + (bbox[2]/2)))
                    midy = (int(bbox[1] + (bbox[3]/2)))
		    errx = (320/2) - midx
		    erry = (240/2) - midy
		    print errx, erry 
                    self.motor.motor_cmd(errx,erry)

	    	self.vs.pub_image(frame)
	    except KeyboardInterrupt:
    		print('interrupted!')
		self.vs.stop()
		sys.exit() 

    def init_tracker(self,bbox):
	frame = self.vs.read()
	self.tracker.init(frame,bbox)
		

	
if __name__ == '__main__' : 
 	obj_trk = object_tracking()
	bbox = (186, 66, 14, 33) 
	obj_trk.init_tracker(bbox)
	obj_trk.track_object()		
