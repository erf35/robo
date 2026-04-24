from serial.tools import list_ports
import dobotplus_me as bot
import position_capture as pc
import time


available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
if not available_ports:
	raise RuntimeError('No serial ports detected for Dobot')

port = available_ports[0].device
device = bot.Dobot(port=port)       #zasek tady
device.set_ir(enable=True)

while True:
    print(f'IR: {device.get_ir()}')
    time.sleep(0.5)