
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
while True:
    if i ==4:
        i=0
    pocet_kostek  = i * 30
    adjst = i*5
    device.move_to(x-adjst,y+pocet_kostek-adjst,vyska_kostka,r,True)
    device.suck(True)
    device.move_to(x,y+pocet_kostek,z+60,r,True)
    device.move_to(x+posun,y,z+60,r,True)
    device.move_to(x+posun,y,vyska_kostka+pocet_kostek,r,True)
    device.suck(False)
    device.move_to(x+posun,y,z+60,r,True)
    device.move_to(x,y,z+60,r,True)
    print(i)
    i+=1




