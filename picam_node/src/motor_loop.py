import time
import sys
from motor_cmd import motor_ctrl

# Angle , speed, direction
motor = motor_ctrl()

for loop in range(1,10):
    for angle in range(0,30):
    	motor.motor_cmd(5, 0)
    	time.sleep(.5) 
    	print angle
    for angle in range(0,30):
    	motor.motor_cmd(-5, 0)
    	print angle
    	time.sleep(.5) 
    for angle in range(0,30):
    	motor.motor_cmd(-5, 0)
    	print angle
    	time.sleep(.5) 
    for angle in range(0,30):
    	motor.motor_cmd(5, 0)
    	time.sleep(.5) 
    	print angle
