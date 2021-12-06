import motion
import argparse
import time
from naoqi import ALProxy
robotIP = "127.0.0.1"
PORT = 9559

motionProxy = ALProxy("ALMotion", robotIP, PORT)


# Example showing how to get the position of the top camera
name            = "RArm"
frame           = motion.FRAME_TORSO
useSensorValues = True
postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
postureProxy.goToPosture("StandInit", 0.5)
result          = motionProxy.setPosition(name, frame, [0.21852481365203857, -0.11097142845392227, 0.08776913583278656,0,0,0], 1, 7)
#result          = motionProxy.getPosition(name, frame, useSensorValues)
# print "Position of", name, " in World is:"
# print result
