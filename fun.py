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
result          = motionProxy.setPosition(name, frame, [0.03202886071619739, 0.019516413309122797, -0.10533551986549275, 0, 0, 0], 1, 7)
# TODO: Take into account the position of the head when making ratios dummy! The HMD is relative to the HMD, NAO to his torso.
# result          = motionProxy.getPosition(name, frame, useSensorValues)
# print "Position of", name, " in World is:"
# print result
