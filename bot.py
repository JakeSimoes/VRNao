import sys
import math
from klampt import *
from klampt import RobotPoser
from klampt.vis.glcommon import GLWidgetPlugin
from klampt import vis
from klampt.math import vectorops,so3,se3
from klampt.model.subrobot import SubRobotModel
from klampt.model import ik
from klampt.plan import robotplanning
from klampt.vis import editors
world = WorldModel()
world.loadFile("nao_rob/nao.rob")
robot= world.robot(0)
base_link = robot.link(4)
base_link.setTransform([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
base_link.setAxis([0.0, 0.0, 0.0])

link = robot.link(69)
link2 = robot.link(39)

"""
Change the world position to adjust the arm's objective
Shift to zoom
Ctrl to Pan
"""

#target = link.getWorldPosition([0,0,0])
# Large numbers break the simulation!!!
target = [0.02438293019835301, -0.25779791993309, 0.1]

obj = ik.objective(link,local=[0,0,0],world=target, t=[0,0,0])
if not ik.solve_global(obj,iters = 10000,tol=1e-3,numRestarts=500, activeDofs=[65,66,67,68,69]):
        print("IK failure!")
# base_link.setTransform([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
# print(base_link.getWorldPosition([0,0,0]))
vis.add("world",world)    #shows the robot in the solved configuration
vis.add("obj", base_link.getWorldPosition([0,0,0]))
vis.setAttribute("obj","type","Vector3")
vis.setColor("obj",1,0,0)  #turns the target point red
vis.add("Hand",link.getWorldPosition([.05,0,0]))
vis.setAttribute("Hand","type","Vector3")
vis.setColor("Hand",1,0,0)  #turns the target point red

print(link.getWorldPosition([1,0,0]))
vis.dialog()