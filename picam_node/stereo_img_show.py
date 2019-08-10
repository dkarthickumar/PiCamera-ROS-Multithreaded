#
# script to decode and show stereo image and alpha blended image
#
#!/usr/bin/python

import sys,time 
import numpy as np
from scipy.ndimage import filters

import cv2

import roslib
import rospy

import threading

#from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image

VERBOSE=True

right_event = threading.Event()
left_event = threading.Event()

right_image = None
left_image = None


class streo_image_show:

    def __init__(self):
	self.subscriber = rospy.Subscriber("/camera_left/image", Image, self.left_callback, queue_size = 1 )
	if VERBOSE:
	    print "subscrbed to /camera_left/image/"

	self.subscriber = rospy.Subscriber("/camera_right/image", Image, self.right_callback, queue_size = 1 )
	if VERBOSE:
	    print "subscrbed to /camera_right/image"
	

    def img_show_alpha(self, right_event, left_event):
	while True:
	    if VERBOSE:
	        print 'waiting for event'
	    right_event_set = right_event.wait()
	    left_event_set = left_event.wait()
	    if VERBOSE:
	        print 'both events are set' 

	    dst = cv2.addWeighted(image_right, 0.5, image_left, 0.5, 0)	    

	    cv2.imshow('cv_img_right', image_right)
	    cv2.imshow('cv_img_left', image_left)
	    cv2.imshow('cv_img_dst', dst)
	    ch = cv2.waitKey(1)
	    if ch == 27:
		cv2.destroyAllWindows()
		break	

	    right_event.clear()
	    left_event.clear()

	

    def right_callback(self, ros_data):
	if VERBOSE:
	    print 'received right image' 

	np_arr = np.fromstring(ros_data.data, np.uint8)
	global image_right
	image_right = cv2.imdecode(np_arr, 1)
	right_event.set()	
	#cv2.imshow('cv_img_right', image_right)
	#cv2.waitKey(1)
	
    def left_callback(self, ros_data):
	if VERBOSE:
	    print 'received left image'

	np_arr = np.fromstring(ros_data.data, np.uint8)
	global image_left
	image_left = cv2.imdecode(np_arr, 1)
	left_event.set()
	#cv2.imshow('cv_img_left', image_left)
	#cv2.waitKey(1)
	

def main(args):
    sis = streo_image_show()
    rospy.init_node('image_show', anonymous=True)


    t1 = threading.Thread(target=sis.img_show_alpha, args=(right_event,left_event) )
    t1.start()
	
    try:
	rospy.spin()
    except KeyboardInterrupt:
	print "shutting down ROS stero image viewer"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
