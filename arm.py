import math
import time
import zmq
import numpy
import openvr
import pickle
from PIL import Image
from PIL import ImageOps
from OpenGL.GL import *
from OpenGL.GLUT import *
from threading import Thread
from scipy.spatial.transform import Rotation as R
from klampt import *
from klampt import vis
from klampt.model import ik


# Convert the 3x4 position/rotation matrix to a x,y,z location and the appropriate Euler angles (in radians)
def convert_to_radians(pose_mat):

    x = pose_mat[0][3]
    y = pose_mat[1][3]
    z = pose_mat[2][3]
    return [x,y,z]

center = 0
poses = []  # Will be populated with proper type after first call
# The next four lines create the Overlay and set its distance
openvr.init(openvr.VRApplication_Scene)
openvr.init(openvr.VRApplication_Overlay)
system = openvr.IVRSystem()
handle = openvr.VROverlay().createOverlay("foo", "bar")  # creates the overlay
openvr.VROverlay().setOverlayWidthInMeters(handle, 1.0)  # sets overlay size

poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
# the following lines convert the input to a numpy array, splice it to get
# only the data we need and then converts that euler to x,y,z
arr = numpy.array(list(hmd_pose.mDeviceToAbsoluteTracking))

arr = openvr.HmdMatrix34_t  # a reference to the data type
# creates an array structure that will be put into a HmdMatrix34 variable.
bar = arr((1.0, 0, 0, 0), (0, 1.0, 0, -0.05), (0, 0, 1.0, -0.5))
test = openvr.Structure.__new__(openvr.HmdMatrix34_t)  # creating a empty var
test._setArray(bar)  # setting the empty HmdMatrix34 var to the bar array.
# sets the overlays position to be relative to the headset
openvr.VROverlay().setOverlayTransformTrackedDeviceRelative(handle,
                                                            openvr.k_unTrackedDeviceIndex_Hmd,
                                                            test)

while True:
    _, leftControllerState = system.getControllerState(
        system.getTrackedDeviceIndexForControllerRole(openvr.TrackedControllerRole_LeftHand))
    _, rightControllerState = system.getControllerState(
        system.getTrackedDeviceIndexForControllerRole(openvr.TrackedControllerRole_RightHand))
    poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
    hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
    lc_pose = poses[openvr.k_EButton_IndexController_A]
    rc_pose = poses[openvr.k_EButton_IndexController_B]
    if True:
        controller_position = convert_to_radians(list(lc_pose.mDeviceToAbsoluteTracking))
        HMD_position = convert_to_radians(list(hmd_pose.mDeviceToAbsoluteTracking))
        print('Controller: ', controller_position, 'HMD: ', HMD_position)
        position = [0, 0, 0]
        for index, i in enumerate(HMD_position):
            if i > controller_position[index]:
                if controller_position[index] < 0:
                    position[index] = -(i - controller_position[index])
                else:
                    position[index] = i - controller_position[index]
            else:
                if controller_position[index] < 0:
                    position[index] = -(controller_position[index] - i)
                else:
                    position[index] = controller_position[index] - i

        print(rightControllerState.rAxis[0].y,rightControllerState.rAxis[0].x)
        time.sleep(0.1)







openvr.shutdown()
