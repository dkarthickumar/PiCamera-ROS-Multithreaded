import sys
from motor_cmd import motor_ctrl

# Angle , speed, direction
print( int(sys.argv[1]) , int(sys.argv[2]))
motor = motor_ctrl()
motor.motor_cmd(int(sys.argv[1]), int(sys.argv[2]))
