#Magician
import math

# nastaveni parametru
dType.SetPTPJointParams(api,200,200,200,200,200,200,200,200,0)
dType.SetPTPCoordinateParams(api,200,200,200,200,0)
dType.SetPTPJumpParams(api, 10, 200,0)
dType.SetPTPCommonParams(api, 100, 100,0)
pos = dType.GetPose(api)
z = 0
x = pos[0]
y = pos[1]
rHead = pos[3]
r = 30
krok = 30
for i in range(0,int(math.pi*2*krok+2)):
 l = i/krok
 xn = x + r*math.cos(l)
 yn = y + r*math.sin(l)
 dType.SetPTPCmd(api, 2, xn, yn, z-60, rHead, 1)
