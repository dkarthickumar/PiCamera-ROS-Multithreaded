import serial
import struct
import os
import time

class motor_ctrl:

    #
    # controls the motro based on the rasp pi 
    #
    def motor_cmd(self, angle_r_l, angle_u_d):

    	camera = os.environ["PI_CAMERA"]
	if (camera == "camera_left"):
       	    start_byte = 'l'
       	elif (camera == "camera_right"):
	    start_byte = 'r'
    
        cmd = struct.pack('cbb', start_byte, angle_r_l, angle_u_d) 
        self.port.write(cmd)
	ret = self.port.read_until(size=1)   
	if ret == '':
	    print('timed out')
	if ret == 'N':
	    print('Nak')
	if ret == 'A':
	    print('Aak')

    def motor_stop(self):
        cmd = struct.pack('cbb', 's', 0, 0) 
        self.port.write(cmd)
	ret = self.port.read_until(size=1)   
	if ret == '':
	    print('timed out')
	if ret == 'N':
	    print('Nak')
	if ret == 'A':
	    print('Aak')
	

    def motor_cmd_all(self,camera, angle_r_l, angle_u_d):

	if (camera == "camera_left"):
       	    start_byte = 'l'
       	elif (camera == "camera_right"):
	    start_byte = 'r'
	if (camera == "camera_up_down"):
       	    start_byte = 'u'
	if (camera == "camera_stop"):
       	    start_byte = 's'
    
        cmd = struct.pack('cbb', start_byte, angle_r_l, angle_u_d) 
        self.port.write(cmd)
	ret = self.port.read_until(size=1)   
	if ret == '':
	    print('timed out')
	if ret == 'N':
	    print('Nak')
	if ret == 'A':
	    print('Aak')


    def get_motor_angles(self):
	cmd = struct.pack('cbb', 'a', 0 ,0)
	self.port.write(cmd)
	if ret == '':
	    print('timed out')
	if ret == 'N':
	    print('Nak')
	if ret == 'A':
	    print('Aak')
	
    def __init__(self):
        self.port = serial.Serial("/dev/ttyUSB0",baudrate=115200, timeout=3.0)
