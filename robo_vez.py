
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
vyska_kostka =-47
posun = 60
device.suck(False)
i = 0
flag = 0
while True:
    pocet_kostek  = i * 30
    x_adjst = i*5
    y_adjst = i*4
    z_mov = 100
    if flag == 0:
        device.move_to(x-x_adjst,y+pocet_kostek-y_adjst,vyska_kostka,r,True)
        device.suck(True)
        device.move_to(x,y+pocet_kostek,z+z_mov,r,True)
        device.move_to(x+posun,y,z+z_mov,r,True)
        device.move_to(x+posun,y,vyska_kostka+pocet_kostek,r,True)
        device.suck(False)
        device.move_to(x+posun,y,z+z_mov,r,True)
        device.move_to(x,y,z+z_mov,r,True)
        i+=1
        if i == 4:
            i=0

device.close()
