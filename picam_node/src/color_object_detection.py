#!/bin/env python
#
# Script to object tracking in the frame using color filtering method 
#
import picam_pub as picam
import cv2
import sys
from motor_cmd import motor_ctrl
import rospy
from std_msgs.msg import Float32MultiArray, MultiArrayDimension
import numpy as np 

class color_object_detection():
    def __init__(self):
        self.vs = picam.PiVideoStream(frame_size=(320, 240), resolution=(1280, 720), framerate=30, ROS=True).start()
        self.motor = motor_ctrl()
        rospy.Subscriber('roi_hist_pub',Float32MultiArray , self.get_hist_data)
        print('subcribed') 
        self.hist_ready = False
        self.hist = []
        self.term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

    def detect_object(self):
        while True:
            try:
                frame = self.vs.read()
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                if self.hist_ready:
                    mask = cv2.calcBackProject([hsv], [0, 1], self.hist, [0, 180, 0, 256], 1)
                    (_, cnts, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    ret, track_window = cv2.CamShift(dst, track_window, term_crit)
                    pts = cv2.boxPoints(ret)
                    pts = np.int0(pts)
                    frame = cv2.polylines(frame,[pts],True,255,2)

                self.vs.pub_image(frame)
            except KeyboardInterrupt:
                print('interrupted!')
                self.vs.stop()
                sys.exit()

    def get_hist_data(self,data):
        print('callback called')
        self.hist = np.asarray(data.data, 'float32').reshape(180,256)
        #print(self.hist)
        self.hist_ready = True

if __name__ == '__main__':
    clr_obj_dect = color_object_detection()
    clr_obj_dect.detect_object()
