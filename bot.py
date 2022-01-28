from klampt import *
from klampt import vis
from klampt.model import ik
import math

world = WorldModel()
world.loadFile("nao_rob/nao.rob")
robot = world.robot(0)
link = robot.link(69)
#link2 = robot.link(39)
target = [0.16094999999999998, -0.313, 0.5]

obj = ik.objective(link,local=[0,0,0],world=target)
ik.solve_global(obj,iters = 100,tol=1e-3,numRestarts=100, activeDofs=[65,66,67,68,69])
thing = robot.getConfig()[65:69]

print(list(map(math.degrees,thing)))
print(robot.getConfig())

# base_link.setTransform([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
# print(base_link.getWorldPosition([0,0,0]))
vis.add("world",world)    #shows the robot in the solved configuration
vis.add("obj", obj)
vis.setAttribute("obj","type","Vector3")
vis.setColor("obj",1,0,0)  #turns the target point red
vis.add("Hand",link.getWorldPosition([0,0,0]))
vis.setAttribute("Hand","type","Vector3")
vis.setColor("Hand",1,0,0)  #turns the target point red
vis.dialog()
# print(link.getWorldPosition([1,0,0]))
