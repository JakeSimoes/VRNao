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
        result = videoDevice.getImageRemote(captureDevice);
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
angle1 = 1
angle2 = 1
thread = Thread(target=visionThread)  # makes a thread for the imageThread function
thread.start()
tts = ALProxy("ALTextToSpeech", ip, port)
motionProxy = ALProxy("ALMotion", ip, port)
motionProxy.setStiffnesses('Head', 1.0)
process = subprocess.Popen("""C:/Python38/python.exe vr.py""",
                           stdout=subprocess.PIPE)

while True:
    # TODO: Socket the headset connection?
    for line in iter(process.stdout.readline,
                     ''):  # replace '' with b'' for Python 3
        if "Headset:  " in line and "[I]" not in line:
            headline = line
            sys.stdout.write(line)
            coords = headline.replace("Headset:  ", "").replace("[", "").replace("]", "").replace(
                "  ", " ").replace("1  ", "").strip().split(" ")
            try:
                angle2 = math.radians(-1.0 * float(coords[0]) - 10)
            except:
                pass
            try:
                angle1 = math.radians(float(coords[1]))
            except:
                pass
            fractionMaxSpeed = 0.3
            # TODO: Fix wrapping yaw values before -80 and after 80
            motionProxy.setAngles("HeadYaw", angle1,
                                  fractionMaxSpeed)
            motionProxy.setAngles("HeadPitch", angle2,
                                  fractionMaxSpeed)

