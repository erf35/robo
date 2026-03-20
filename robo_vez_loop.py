
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
i = -1
while True:
    if i < 3:
        i+=1
    else:
        i = 0
    pocet_kostek_z  = i * 30
    pocet_kostek_x = i*10
    pocet_kostek_y = i*30
    device.move_to(x+pocet_kostek_x,y,vyska_kostka,r,True)
    device.suck(True)
    device.move_to(x,y,vyska_kostka+pocet_kostek_z+10,r,True)
    device.move_to(x+posun,y,vyska_kostka+pocet_kostek_z+10,r,True)
    device.move_to(x+posun,y,vyska_kostka+pocet_kostek_z,r,True)
    device.suck(False)
    device.move_to(x+posun,y,vyska_kostka+pocet_kostek_z+10,r,True)
    device.move_to(x+pocet_kostek_x,y,vyska_kostka+pocet_kostek_z,r,True)
    print(i)

device.close()
