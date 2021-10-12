import numpy
import openvr
import os
import subprocess
from threading import Thread
from scipy.spatial.transform import Rotation as R
import math
import time
import random
# this file handles all the VR data

# def convert_to_euler(pose_mat):
#     yaw = 180 / math.pi * math.atan2(pose_mat[1][0], pose_mat[0][0])
#     pitch = 180 / math.pi * math.atan2(pose_mat[2][0], pose_mat[0][0])
#     roll = 180 / math.pi * math.atan2(pose_mat[2][1], pose_mat[2][2])
#     x = pose_mat[0][3]
#     y = pose_mat[1][3]
#     z = pose_mat[2][3]
#     return [x,y,z,yaw,pitch,roll]

# Convert the 3x4 position/rotation matrix to a x,y,z location and the appropriate Euler angles (in radians)
def convert_to_radians(pose_mat):
    roundfact = 16

    x = pose_mat[0][3]
    y = pose_mat[1][3]
    z = pose_mat[2][3]

    # Algorhitm 1

    # read here: https://steamcommunity.com/app/358720/discussions/0/343787920117426152/
    pitch = math.atan2(pose_mat[2][1], pose_mat[2][2])
    yaw = math.asin(pose_mat[2][0])
    roll = math.atan2(-pose_mat[1][0], pose_mat[0][0])
    return [x,y,z,yaw, pitch, roll]


def imageThread():
    # global variables are are no no but are required for threads
    # to communicate...
    global seed
    global call
    while True:
        # opens a subprocess which runs grabImageFunc.py passing the call number
        # as an argument to have it output an image with that call number
        process = subprocess.Popen("F:/Python27/python.exe grabImageFunc.py {} {}"
                                   .format(seed, call), stdout=None)
        process.wait()  # waits until the subprocess is done to insure the
                        # overlay can access the file
        time.sleep(0.1)
        overlayRefresh()
        call += 1
        try:
            if call > 2:
                os.remove("{}camImage{}.png".format(str(seed), str(call - 2)))
        except:
            pass

def overlayRefresh():
    # global variables are are no no but are required for threads
    # to communicate...
    global call
    openvr.VROverlay().clearOverlayTexture(handle) # clears the last image
    # sets the overlay image to the image with the current call number
    openvr.VROverlay().setOverlayFromFile(handle,
                                          'C:\\Users\\JakeS\\Desktop\\NAO\\{}camImage{}.png'.format(
                                              seed, call))
    # refreshes the overlay
    openvr.VROverlay().showOverlay(handle)

seed = random.randint(0,100000)
call = 0  # initializes the call to start at 0
poses = []  # will be populated with proper type after first call
# The next four lines create the Overlay and set its distance
openvr.init(openvr.VRApplication_Scene)
openvr.init(openvr.VRApplication_Overlay)
handle = openvr.VROverlay().createOverlay('foo', "bar")  # creates the overlay
openvr.VROverlay().setOverlayWidthInMeters(handle, 1.0)  # sets overlay size
arr = openvr.HmdMatrix34_t  # a reference to the data type
# creates an array structure that will be put into a HmdMatrix34 variable.
bar = arr((1.0, 0, 0, 0), (0, 1.0, 0, 0), (0, 0, 1.0, -0.7))
test = openvr.Structure.__new__(openvr.HmdMatrix34_t)  # creating a empty var
test._setArray(bar)  # setting the empty HmdMatrix34 var to the bar array.
# sets the overlays position to be relative to the headset
openvr.VROverlay().setOverlayTransformTrackedDeviceRelative(handle,
                                                            openvr.k_unTrackedDeviceIndex_Hmd,
                                                            test)
thread = Thread(target=imageThread)  # makes a thread for the imageThread function
thread.start()  # starts the imageThread which will update the video feed.
while True:
    poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
    hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
    # the following lines convert the input to a numpy array, splice it to get
    # only the data we need and then converts that euler to x,y,z
    arr = numpy.array(list(hmd_pose.mDeviceToAbsoluteTracking))
    r = R.from_matrix(arr[0:, 0:-1])
    print("\nHeadset: ",r.as_euler('xyz', degrees=True))

    # poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
    # lc_pose = poses[openvr.k_EButton_IndexController_B]
    # arr = numpy.array(list(lc_pose.mDeviceToAbsoluteTracking))
    # agh = convert_to_radians(arr)
    #
    # try:
    #     print("\nController 1: ", agh)
    # except:
    #     pass
    # poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
    # rc_pose = poses[openvr.k_EButton_IndexController_A]
    # arr = numpy.array(list(lc_pose.mDeviceToAbsoluteTracking))
    # try:
    #     print("Controller 2: ", convert_to_euler(arr))
    # except:
    #     pass





openvr.shutdown()
