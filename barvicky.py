from serial.tools import list_ports
import pydobotplus as bot
import position_capture as pc

POSITION_FILE = "positions.json"

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
if not available_ports:
	raise RuntimeError('No serial ports detected for Dobot')

port = available_ports[0].device
device = bot.Dobot(port=port)
device.set_color(enable=True, version=1)

try:
	pozice = pc.get_positions_from_file(POSITION_FILE)
except FileNotFoundError:
	device.close()
	raise RuntimeError(
		f"Missing {POSITION_FILE}. Run capture_positions.py once to save positions."
	)

nad_senzorem = (pozice["senzor"][0], pozice["senzor"][1], pozice["senzor"][2]+50)

device.move_to(*nad_senzorem, wait=True)
device.move_to(*pozice["senzor"], wait=True)
color = device.get_color()
if color[0] == 1:
    print("Detected red")
device.suck(True)
device.move_to(*nad_senzorem, wait=True)
device.move_to(*pozice["odkladani"], wait=True)
device.suck(False)




device.suck(False)

device.close()

