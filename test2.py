robots = [0.16094999999999998, -0.113, 0.1]
HMDs = [0.21623797714710236, 0.18147623538970947, 0.5982634276151657]

ratiox = robots[0]/HMDs[2]

HMDtoRobot = [2,0,1]

# print(ratiox)

robotr = [0.02438293019835301, -0.25779791993309, 0.1]
HMDr = [0.21623797714710236, 0.18147623538970947, 0.5982634276151657]

ratioy = robots[1]/HMDr[0]

# print(ratioy)

robotu = [0.16094999999999998, -0.113, 0.1]
HMDu = [0.21623797714710236, 0.18147623538970947, 0.5982634276151657]

ratioz = robots[2]/HMDu[1]

# print(ratioz)

ratios = [ratiox,ratioy,ratioz]



for index, i in enumerate(HMDtoRobot):
    print(HMDr[i]*ratios[index])
