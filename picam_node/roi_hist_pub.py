#!/bin/env python
#
# Script to generate ROI histogram and publish to stream
#
import cv2
import rospy
import numpy as np
#from rospy.numpy_msg import numpy_msg
#from rospy_tutorials.msg import Floats
from std_msgs.msg import Float32MultiArray, MultiArrayDimension

class RoiHistPub:
    def __init__(self):
        rospy.init_node('roi_histogram', anonymous=False)
        self.pub = rospy.Publisher('roi_hist_pub', Float32MultiArray, queue_size=1)
        self.rate = rospy.Rate(1)

    def hist_pub(self):
        img = cv2.imread('/home/karthic/Pictures/green_egg.png', cv2.IMREAD_COLOR)
        roi = cv2.selectROI(img)
        roi_img = img[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        roi_hsv = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)
        roi_hist = cv2.calcHist([roi_hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])

        mat = Float32MultiArray()
        mat.layout.dim = []
        dims = np.array(roi_hist.shape)
        dims_size = dims.prod()/float(roi_hist.nbytes)

        for i in range(0, len(dims)):
            mat.layout.dim.append(MultiArrayDimension())
            mat.layout.dim[i].size = dims[i]
            mat.layout.dim[i].stride = dims[i:].prod()/dims_size
            mat.layout.dim[i].label = 'dim_%d'%i

        while not rospy.is_shutdown():
            #publish histogram at specified rate
            mat.data = np.frombuffer(roi_hist.tobytes(),'float32')
            self.pub.publish(mat)
            self.rate.sleep()

if __name__ == '__main__':
    hist = RoiHistPub()
    hist.hist_pub()

