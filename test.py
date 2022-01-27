robots = [0.16094999999999998, -0.113, 0.1]
HMDs = [0.21623797714710236, 0.18147623538970947, 0.5982634276151657]
ratiox = robots[0]/HMDs[2]

robotr = [0.02438293019835301, -0.25779791993309, 0.1]
HMDr = [0.6773498952388763, 0.10197412967681885, 0.1579793393611908]
ratioy = robotr[1]/HMDr[0]

robotu = [-0.015247020552836821, -0.113, 0.2602261865746713]
HMDu = [0.4954894036054611, 0.94499671459198, 0.29504750669002533]
ratioz = robotu[2]/HMDu[1]

ratios = [ratiox,ratioy,ratioz]
HMDtoRobot = [2,0,1]

relative_hmd = [0.4954894036054611, 0.94499671459198, 0.29504750669002533]
relative_robot = []
for index, i in enumerate(HMDtoRobot):
    relative_robot.append(relative_hmd[i]*ratios[index])

#relative_robot[2] += 0.1264999955892563
print(relative_robot)