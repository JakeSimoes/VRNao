from klampt import *
from klampt.model import ik
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


"""This file handles all of the VR data and interactions with the headset"""


def read_texture(image_data):
    # Set the dimensions of the image
    width = 320
    height = 240
    # Receive the image and clean it up
    img = Image.fromarray(image_data).convert('RGBA')
    img = ImageOps.flip(img)
    data = numpy.array(list(img.getdata()), numpy.int8)
    # After texture_id is defined it is
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    # Texture Parameter Setup...
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
    # Sending data to the buffer...
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture_id, 0)
    return texture_id


# Convert the 3x4 position/rotation matrix to a x,y,z location and the appropriate Euler angles (in radians)
def convert_to_cartesian(pose_mat):
    x = pose_mat[0][3]
    y = pose_mat[1][3]
    z = pose_mat[2][3]
    return [x, y, z]


def convert_to_radians(pose_mat):
    global center
    r_w = math.sqrt(max(0, 1 + pose_mat[0][0] + pose_mat[1][1] + pose_mat[2][2])) / 2
    r_x = math.sqrt(max(0, 1 + pose_mat[0][0] - pose_mat[1][1] - pose_mat[2][2])) / 2
    r_y = math.sqrt(max(0, 1 - pose_mat[0][0] + pose_mat[1][1] - pose_mat[2][2])) / 2
    r_z = math.sqrt(max(0, 1 - pose_mat[0][0] - pose_mat[1][1] + pose_mat[2][2])) / 2
    r_x *= math.copysign(1, r_x * (-pose_mat[2][1] + pose_mat[1][2]))
    r_y *= math.copysign(1, r_y * (-pose_mat[0][2] + pose_mat[2][0]))
    r_z *= math.copysign(1, r_z * (pose_mat[1][0] - pose_mat[0][1]))

    x = pose_mat[0][3]
    y = pose_mat[1][3]
    z = pose_mat[2][3]
    result = ((r_y * 180) + 180)

    if center > 180:
        upperbound = center - 180
    else:
        upperbound = 180 + center

    if result > center and result < upperbound:
        return [-min(abs(result - center), 360 - abs(result - center)), (r_x*40)]
    else:
        return [min(abs(result - center), 360 - abs(result - center)), (r_x*40)]


def center_headset(pose_mat):
    global center
    r_y = math.sqrt(max(0, 1 - pose_mat[0][0] + pose_mat[1][1] - pose_mat[2][2])) / 2
    r_y *= math.copysign(1, r_y * (-pose_mat[0][2] + pose_mat[2][0]))
    center = ((r_y * 180) + 180)



def draw():
    return


def overlay_refresh():
    # Connecting to the main.py image socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    # Initializing Glut Stuff...
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow("")
    glutHideWindow()
    # A blank function is used as there is no use for the window
    glutDisplayFunc(draw)
    # Setting up a memory buffer for textures
    fb = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fb)
    depth_buffer = glGenRenderbuffers(1)
    glBindRenderbuffer(GL_RENDERBUFFER, depth_buffer)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, 240, 320)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, depth_buffer)
    time.sleep(0.1)
    while True:
        pass
        socket.send(b"Hello")

        #  Get the reply.
        message = socket.recv()
        result = pickle.loads(message, encoding='latin1')  # Decoding latin1 for python 2.7 data conversion
        openvr.VROverlay().clearOverlayTexture(handle)  # Clears the last image
        texture = openvr.Texture_t()  # Create a texture object
        while True:
            try:  # The read_texture func is called in a try statement to catch memory access errors
                texture.handle = read_texture(result)  # Setting the handle attribute to the result of read_texture()
            except Exception as e:
                continue
            finally:
                break
        texture.eType = openvr.TextureType_OpenGL  # Setting the texture type attribute to OpenGL
        texture.eColorSpace = openvr.ColorSpace_Gamma  # Setting the ColorSpace to Gamma as it doesn't crash
        while True:
            try:
                openvr.VROverlay().setOverlayTexture(handle, texture)  # Finally sending the texture to OpenVR
                openvr.VROverlay().showOverlay(handle)  # Making sure to show it!
            except Exception as e:
                continue
            finally:
                break

context2 = zmq.Context()
socket2 = context2.socket(zmq.REP)
socket2.bind("tcp://*:5556")
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
# now setting up the IK solver...
world = WorldModel()
world.loadFile("nao_rob/nao.rob")
robot = world.robot(0)
link = robot.link(69)
HMDtoRobot = [2, 0, 1]
rArmRotations = [0, 0, 0, 0]
thread = Thread(target=overlay_refresh)  # makes a thread for the imageThread function
thread.start()  # starts the imageThread which will update the video feed.
while True:
    # Grabbing VR data
    _, left_controller_state = system.getControllerState(
        system.getTrackedDeviceIndexForControllerRole(openvr.TrackedControllerRole_LeftHand))
    _, right_controller_state = system.getControllerState(
        system.getTrackedDeviceIndexForControllerRole(openvr.TrackedControllerRole_RightHand))
    poses, _ = openvr.VRCompositor().waitGetPoses(poses, None)
    hmd_pose = poses[openvr.k_unTrackedDeviceIndex_Hmd]
    # This grabs that state of the controller
    lc_pose = poses[openvr.k_EButton_IndexController_B]
    rc_pose = poses[openvr.k_EButton_IndexController_A]
    HMD_rotation = convert_to_radians(list(hmd_pose.mDeviceToAbsoluteTracking))
    # Grabbing positional data and formatting it
    controller_position = convert_to_cartesian(list(rc_pose.mDeviceToAbsoluteTracking))
    HMD_position = convert_to_cartesian(list(hmd_pose.mDeviceToAbsoluteTracking))
    position = [0, 0, 0]
    for index, i in enumerate(HMD_position):
        if i > controller_position[index]:
            position[index] = -(abs(i - controller_position[index]))
        else:
            position[index] = abs(controller_position[index] - i)
        position[2] = -position[2]
    if bool(right_controller_state.ulButtonPressed >> 2 & 1):
        center_headset(list(hmd_pose.mDeviceToAbsoluteTracking))
    rc_trigger = [right_controller_state.rAxis[1].x]
    #lc_trigger = right_controller_state.rAxis[1].x
    #rc_stick = [right_controller_state.rAxis[0].y, right_controller_state.rAxis[0].x]
    lc_stick = [left_controller_state.rAxis[0].y, left_controller_state.rAxis[0].x]
    # TODO: Implement better ratios for testing
    # TODO: Have ratios be calculated for the users specific arms
    # Scale the coordinates
    ratios = [0.2690286461961894, -0.5225724060631975, -0.5510363369906585]
    relative_robot = []
    for index, i in enumerate(HMDtoRobot):
        relative_robot.append(position[i] * ratios[index])
    # Set them as an objective and solve.
    obj = ik.objective(link, local=[0, 0, 0], world=relative_robot)
    # Iterations are set low so it can be fast, may be weird at times.
    ik.solve_global(obj, iters=100, tol=1e-3, numRestarts=100, activeDofs=[65, 66, 67, 68, 69])
    rArmRotations = robot.getConfig()[65:69]
    final_packet = HMD_rotation + rArmRotations + rc_trigger + lc_stick
    message = socket2.recv()
    socket2.send_string("{} {} {} {} {} {} {} {} {}".format(*final_packet))


openvr.shutdown()
