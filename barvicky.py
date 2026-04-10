from serial.tools import list_ports

import pydobotplus as bot

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

device = bot.Dobot(port=port)
device.set_color(enable=True, version=1)

while True:
    print(device.get_color())
    
    
