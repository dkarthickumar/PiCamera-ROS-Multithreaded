import sys
from motor_cmd import motor_ctrl

# Angle , speed, direction
print( sys.argv[1] , int(sys.argv[2]))
motor = motor_ctrl()

motor.motor_cmd_all(sys.argv[1], int(sys.argv[2]))
