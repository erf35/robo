
from serial.tools import list_ports

import pydobot


# inicializace
available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[1].device
device = pydobot.Dobot(port=port, verbose=True)

# urceni zakladnich pozic
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

# hlavni loop programu
while True:
    # posouvani pozic mezi jednotlivymi kostkami
    pocet_kostek  = i * 29
    x_adjst = i*4
    y_adjst = i*4
    z_mov = 100

    # staveni veze
    if flag == 0:
        device.move_to(x-x_adjst,y+pocet_kostek-y_adjst,vyska_kostka,r,True) # posun nad kostku ve skladu
        device.suck(True) # spusteni prisavky

        # posun kostky na vez
        device.move_to(x,y+pocet_kostek,z+z_mov,r,True)
        device.move_to(x+posun,y,z+z_mov,r,True)
        device.move_to(x+posun,y,vyska_kostka+pocet_kostek,r,True)
        device.suck(False) # vypnuti prisavky

        # posun zpet nad sklad
        device.move_to(x+posun,y,z+z_mov,r,True)
        device.move_to(x,y,z+z_mov,r,True)
        i+=1

        # po kolika kostkach se ma loop zmenit na rozkladani veze
        if i == 4:
            flag = 1
            
    # rozkladani veze
    else:
        i-=1
        device.move_to(x+posun,y,z+z_mov,r,True)
        device.move_to(x+posun,y,vyska_kostka+pocet_kostek,r,True)
        device.suck(True)
        device.move_to(x+posun,y,z+z_mov,r,True)
        device.move_to(x,y,z+z_mov,r,True)
        device.move_to(x-x_adjst,y+pocet_kostek-y_adjst,vyska_kostka,r,True)
        device.suck(False)

        
        if i == 0:
            flag = 0




