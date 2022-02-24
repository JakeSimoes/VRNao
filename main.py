import subprocess
import sys
import math
from naoqi import ALProxy
import motion
import time
import pickle
import numpy as np
import cv2
import zmq
from threading import Thread

"""This file handles all the Nao interactions"""

"""ROBOT IP"""
ip = "127.0.0.1"
port = 9559


def armThread():
    # TODO: Add gripper and wrist rotation control.
    # wait a good amount of time for variables to get initialized
    while True:
        if 'rPitch' not in globals():
            time.sleep(1)
        else:
            break
    global rPitch, rRoll, rYaw, reRoll, lPitch, lRoll, lYaw, leRoll, rTrig, lTrig, motionProxy
    while True:
        motionProxy.setAngles("RShoulderPitch", -rPitch,
                              0.1)
        motionProxy.setAngles("RShoulderRoll", rRoll,
                              0.1)
        motionProxy.setAngles("RElbowYaw", rYaw,
                              0.1)
        motionProxy.setAngles("RElbowRoll", reRoll,
                              0.1)
        motionProxy.setAngles("LShoulderPitch", -lPitch,
                              0.1)
        motionProxy.setAngles("LShoulderRoll", lRoll,
                              0.1)
        motionProxy.setAngles("LElbowYaw", lYaw,
                              0.1)
        motionProxy.setAngles("LElbowRoll", leRoll,
                              0.1)
        motionProxy.setAngles("RHand", rTrig, 0.1)
        motionProxy.setAngles("LHand", lTrig, 0.1)
        time.sleep(0.1)


def visionThread():
    global ip
    global port
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    # get NAOqi module proxy
    videoDevice = ALProxy('ALVideoDevice', ip, port)

    # subscribe top camera
    AL_kTopCamera = 0
    AL_kQVGA = 1  # 320x240
    AL_kBGRColorSpace = 13
    captureDevice = videoDevice.subscribeCamera(
        "test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)

    # create image
    width = 320
    height = 240
    image = np.zeros((height, width, 3), np.uint8)

    while True:
        # get image
        result = videoDevice.getImageRemote(captureDevice)
        if result == None:
            print('cannot capture.')
        elif result[6] == None:
            print('no image data string.')
        else:

            # translate value to mat
            values = result[6]
            i = 0
            for y in range(0, height):
                for x in range(0, width):
                    image.itemset((y, x, 0), ord(values[i + 0]))
                    image.itemset((y, x, 1), ord(values[i + 1]))
                    image.itemset((y, x, 2), ord(values[i + 2]))
                    i += 3
            message = socket.recv()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            socket.send(pickle.dumps(image))


# this file is the main file which controls NAO
motionProxy = ALProxy("ALMotion", ip, port)
postureProxy = ALProxy("ALRobotPosture", ip, 9559)
postureProxy.goToPosture("StandInit", 0.5)
motionProxy.setStiffnesses('Head', 1.0)
# starts both threads for controlling vision and arm movement
thread = Thread(target=visionThread)  # makes a thread for the imageThread function
thread.start()
thread2 = Thread(target=armThread)  # makes a thread for the imageThread function
thread2.start()
# starting up the VR file
# process = subprocess.Popen("""C:/Python38/python.exe vr.py""",
#                            stdout=subprocess.PIPE)
process = subprocess.Popen("""C:/Users/Jake Simoes/AppData/Local/Programs/Python/Python39/python.exe vr.py""",
                           stdout=subprocess.PIPE)
# connecting to the VR data socket
context2 = zmq.Context()
socket2 = context2.socket(zmq.REQ)
socket2.connect("tcp://localhost:5556")
while True:
    socket2.send(" ")
    message = socket2.recv_string()
    print(message)
    yaw, pitch, lPitch, lRoll, lYaw, leRoll, rPitch, rRoll, \
    rYaw, reRoll, lTrig, rTrig, lY, lX, rY, rX = map(float, message.split(" "))
    motionProxy.setAngles("HeadYaw", math.radians(yaw),
                          0.3)
    motionProxy.setAngles("HeadPitch", math.radians(pitch),
                          0.3)
    if lY > 0.1 or lX > 0.1 or lY < -0.1 or lX < -0.1:
        motionProxy.setWalkTargetVelocity(lY, -lX, 0.0, 0.0)
    else:
        motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)
