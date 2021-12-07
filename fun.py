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
result          = motionProxy.setPosition(name, frame, [0.120282462081, 0.232241273302, 0.149190879559, 0, 0, 0], 1, 7)
# TODO: Take into account the position of the head when making ratios dummy! The HMD is relative to the HMD, NAO to his torso.
#result          = motionProxy.getPosition(name, frame, useSensorValues)
# print "Position of", name, " in World is:"
# print result
