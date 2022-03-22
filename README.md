# VRNao
![alt text](https://user-images.githubusercontent.com/60676244/159024777-518b0113-d8c0-4f8b-847b-38cabd4b3222.png)

This is a Python program which allows a user to use a SteamVR compatible VR headset to control a NAO robot.
Other's have done the same but have used ROS through Linux which cripples accessibility. VRNAO is packaged as an EXE so anyone can easily run it

Using the Python binding for OpenVR and the Python 2.7 naoqi library it's possible to control the NAO robot with a headset. Due to pyopenVR not supporting python 2.7 a network socket is used to exchange information on the headset and controllers. Then using the data along with Klampt for IK solving, the user can view the robot's cameras through the headset, move its arms with the controller, and make it walk with the sticks.

Some solutions to problems are code snippets from others which should be cited.

EXE DOWNLOAD: https://drive.google.com/file/d/1li8-zqVsgT7ncOITcOvQTkv4UfmRBsgR/view?usp=sharing

# Features
- View NAO's cameras through the headset, move his head with HMD movement.
- Position NAO's arms using the controllers.
- Grip button will reset your head positioning.
- Trigger button will open NAO's hands once pushed down.
- Left stick allows forward, backward and strafing movements.
- Right stick will have NAO walk in the general direction.

# Bugs/Pitfalls
There are several known bugs which will likely not be fixed as this is an inconsequential project.
- Some kind of gimbal lock has the head rotation break at certain positions.
- Currently arm positioning cannot be set by the user, I had a good algorithm but lost it.
- When the headset is taken off and the program is running NAO may fling his arms. Make sure to turn off the program before removing the HMD.
- The NAO vision has a low framerate, this is partly a limitation of NAO.
