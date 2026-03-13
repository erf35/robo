import pydobot as bot
from serial.tools import list_ports
import os
import svgpathtools
available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[1].device

device = bot.Dobot(port=port, verbose=True)

