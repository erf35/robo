
from serial.tools import list_ports

import pydobot

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[1].device

device = pydobot.Dobot(port=port, verbose=True)
pozice = device.pose()
x = pozice[0]
y = pozice[1]
z = pozice[2]
r = pozice[3]
vyska_kostka =-50
posun = 60
device.suck(False)
for i in range(4):
    pocet_kostek  = i * 25
    device.move_to(x,y+pocet_kostek,vyska_kostka,r,True)
    device.suck(True)
    device.move_to(x,y+pocet_kostek,z+60,r,True)
    device.move_to(x+posun,y,z+60,r,True)
    device.move_to(x+posun,y,vyska_kostka+pocet_kostek,r,True)
    device.suck(False)
    device.move_to(x+posun,y,z+60,r,True)
    device.move_to(x,y,z+60,r,True)
    print(i)

device.close()
