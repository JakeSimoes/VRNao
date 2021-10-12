import subprocess
import sys
import math
from naoqi import ALProxy
import motion
import time
from threading import Thread

# this file is the main file which controls NAO
chainName = "LArm"
frame = motion.FRAME_ROBOT
useSensor = False
axisMask = 7
angle1 = 1
angle2 = 1
tts = ALProxy("ALTextToSpeech", "127.0.0.1", 9559)
motionProxy = ALProxy("ALMotion", "127.0.0.1", 9559)
process = subprocess.Popen("""C:/Program Files/Python38/python.exe vr.py""",
                           stdout=subprocess.PIPE)


def armThread():
    pass
    # while True:
    #     for line in iter(process.stdout.readline,
    #                      ''):
    #         if "Controller 1:  " in line and "[I]" not in line:
    #             fractionMaxSpeed = 1
    #             sys.stdout.write(line)
    #             armline = line
    #             cont = armline.replace("Controller 1:  ", "").replace("]", "").replace("[",
    #                                                                             "").replace(
    #                 ",", "")
    #             coord = list(map(float, cont.split()))
    #             x, y, z, _, _, _ = coord
    #             if x == 0.0:
    #                 continue
    #             constant = 0.00624797086946079510148647328347
    #             target = [x*-0.03388910584270261663364223270427,y*0.00199719102073177345260041979246,z*-0.01264622217894538614674518607318,0.0,0.0,0.0]
    #             print(target)
    #
    #             try:
    #                 motionProxy.setPositions(chainName, frame, target,
    #                                      fractionMaxSpeed, axisMask)
    #             except Exception as e:
    #                 print(e)
    #             time.sleep(1)
            


thread = Thread(target=armThread)  # makes a thread for the imageThread function
thread.start()

while True:
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
            motionProxy.setAngles("HeadYaw", angle1,
                                  fractionMaxSpeed)
            motionProxy.setAngles("HeadPitch", angle2,
                                  fractionMaxSpeed)

