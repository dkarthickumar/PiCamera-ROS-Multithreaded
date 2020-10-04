#!/bin/env python
#
# Script to generate ROI histogram and publish to stream
#
import cv2
import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

class RoiHistPub:
    def __init__(self):
        rospy.init_node('roi_histogram', anonymous=False)
        self.pub = rospy.Publisher('roi_his_pub', numpy_msg(Floats))
        self.rate = rospy.Rate(1)

    def hist_pub(self):
        img = cv2.imread('/home/karthic/Pictures/green_egg.png', cv2.IMREAD_COLOR)
        roi = cv2.selectROI(img)
        roi_img = img[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        roi_hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
        roi_hist = cv2.calcHist([roi_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

        while not rospy.is_shutdown():
            #publish histogram at specified rate
            self.pub.publish(roi_hist)
            self.rate.sleep()

if __name__ == '__main__':
    hist = RoiHistPub()
    hist.hist_pub()

