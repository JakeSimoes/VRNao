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

ip = raw_input("Enter ROBOT IP or leave blank for localhost.\n")
speed = float(raw_input("Enter speed 0.0-1.0 (Stick to 0.1 for real robots)\n"))
if ip.isspace():
    ip = '127.0.0.1'
port = 9559


def armThread():
    # Wait a good amount of time for variables to get initialized
    while True:
        if 'rPitch' not in globals():
            time.sleep(1)
        else:
            break
    global rPitch, rRoll, rYaw, reRoll, lPitch, lRoll, lYaw, leRoll, rTrig, lTrig, rRot, lRot, motionProxy
    while True:
        motionProxy.setAngles("RShoulderPitch", -rPitch,
                              speed)
        motionProxy.setAngles("RShoulderRoll", rRoll,
                              speed)
        motionProxy.setAngles("RElbowYaw", rYaw,
                              speed)
        motionProxy.setAngles("RElbowRoll", reRoll,
                              speed)
        motionProxy.setAngles("LShoulderPitch", -lPitch,
                              speed)
        motionProxy.setAngles("LShoulderRoll", lRoll,
                              speed)
        motionProxy.setAngles("LElbowYaw", lYaw,
                              speed)
        motionProxy.setAngles("LElbowRoll", leRoll,
                              speed)
        motionProxy.setAngles("RHand", rTrig, 0.1)
        motionProxy.setAngles("LHand", lTrig, 0.1)
        if rRot > .60:
            rRot = 1.7
        elif rRot < -.60:
            rRot = -1.7
        else:
            rRot = rRot * 2

        if lRot > .60:
            lRot = 1.7
        elif lRot < -.60:
            lRot = -1.7
        else:
            lRot = lRot * 2

        motionProxy.setAngles("RWristYaw", rRot, speed)
        motionProxy.setAngles("LWristYaw", lRot, speed)


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
            print('Failed to get image from robot, try restarting the simulation or robot.')
        elif result[6] == None:
            print('Failed to receive valid data from the robot, try restarting the simulation or robot.')
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


motionProxy = ALProxy("ALMotion", ip, port)
postureProxy = ALProxy("ALRobotPosture", ip, 9559)
postureProxy.goToPosture("StandInit", 0.5)
motionProxy.setStiffnesses('Head', 1.0)
# starts both threads for controlling vision and arm movement
thread = Thread(target=visionThread)  # makes a thread for the imageThread function
thread.start()
thread2 = Thread(target=armThread)  # makes a thread for the armThread function
thread2.start()

print("Starting VR process...")
"""OpenVR doesn't work with python 2.7, to move around that issue
   a python 3.8 install with it is used and communicated to via sockets."""

process = subprocess.Popen("vr/vr.exe")
print("Success!")
print("Waiting for VR boot up...")
# connecting to the VR data socket
context2 = zmq.Context()
socket2 = context2.socket(zmq.REQ)
socket2.connect("tcp://localhost:5556")
print("Successfully connected to VR process!")
print("Robot control is live, be cautious to not over stress your robot.\n"
      "Make sure to close the application before taking off the headset.")
while True:
    socket2.send(" ")
    message = socket2.recv_string()
    yaw, pitch, lPitch, lRoll, lYaw, leRoll, rPitch, rRoll, \
    rYaw, reRoll, lTrig, rTrig, lY, lX, rY, rX, lRot, rRot = map(float, message.split(" "))
    motionProxy.setAngles("HeadYaw", math.radians(yaw),
                          0.3)
    motionProxy.setAngles("HeadPitch", math.radians(pitch),
                          0.3)
    if lY > 0.1 or lX > 0.1 or lY < -0.1 or lX < -0.1:
        motionProxy.setWalkTargetVelocity(lY, -lX, 0.0, 0.0)
    elif rY > 0.1 or rX > 0.1 or rY < -0.1 or rX < -0.1:
        motionProxy.moveToward(rY, -rX, 0.0, [["Frequency", 0.5]])
    else:
        motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)
