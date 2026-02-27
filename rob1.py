#Magician
import math

# nastaveni parametru
dType.SetPTPJointParams(api,200,200,200,200,200,200,200,200,0)
dType.SetPTPCoordinateParams(api,200,200,200,200,0)
dType.SetPTPJumpParams(api, 10, 200,0)
dType.SetPTPCommonParams(api, 100, 100,0)

# parkovaci pozice
x = 200
y = 0
z = 0
rHead = pos[3]

# pohyb
for i in range(50):
  dType.SetPTPCmd(api, 2, x, y-70, z, rHead, 1)
  dType.SetPTPCmd(api, 2, x, y-100, z-60, rHead, 1)
  dType.SetPTPCmd(api, 2, x, y, z, rHead, 1)
