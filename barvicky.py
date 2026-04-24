from serial.tools import list_ports
import pydobotplus as bot
import position_capture as pc

POSITION_FILE = "positions.json"

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
if not available_ports:
	raise RuntimeError('No serial ports detected for Dobot')

port = available_ports[0].device
device = bot.Dobot(port=port)       #zasek tady
device.set_color(enable=True, version=1)

try:
	pozice = pc.get_positions_from_file(POSITION_FILE)
except FileNotFoundError:
	device.close()
	raise RuntimeError(
		f"Missing {POSITION_FILE}. Run pozice_barvicky.py once to save positions."
	)

nad_senzorem = (pozice["senzor"][0], pozice["senzor"][1], pozice["senzor"][2]+50)
nad_skladem = (pozice["odkladani"][0], pozice["odkladani"][1], pozice["odkladani"][2]+150)
sklad = (pozice["odkladani"][0], pozice["odkladani"][1], pozice["odkladani"][2])

device.move_to(*nad_skladem, wait=True)
device.move_to(*nad_senzorem, wait=True)
device.move_to(*pozice["senzor"], wait=True)
color = device.get_color()
if color[0] == 1:
    print("Detected red")
elif color[1] == 1:
	print("Deteceted green")
	sklad = (pozice["odkladani"][0], pozice["odkladani"][1]+50, pozice["odkladani"][2])
elif color[2]==1:
	print("Deteceted blue")
	sklad = (pozice["odkladani"][0], pozice["odkladani"][1]-50, pozice["odkladani"][2])
else:
	print("ses kokot, neni validni barva, ted je to cervena, cause fuck you")
	sklad = (pozice["odkladani"][0], pozice["odkladani"][1]-100, pozice["odkladani"][2])
device.suck(True)
device.move_to(*nad_senzorem, wait=True)
device.move_to(*nad_skladem, wait=True)
device.move_to(*sklad, wait=True)
device.suck(False)




device.suck(False)

device.close()

