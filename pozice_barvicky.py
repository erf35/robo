import position_capture as pc
from serial.tools import list_ports
import pydobotplus as bot

# vytvoreni nazvy souboru a ulozenych promenych
POSITION_FILE = "positions.json"
POSITION_NAMES = ("senzor", "odkladani")

# inicializace
def main() -> None:
    available_ports = list_ports.comports()
    print(f'available ports: {[x.device for x in available_ports]}')
    if not available_ports:
        raise RuntimeError('No serial ports detected for Dobot')

    port = available_ports[0].device
    device = bot.Dobot(port=port)

    # ulozeni aktualni pozice robota do souboru 
    pc.capture_positions_to_file(POSITION_NAMES, device, POSITION_FILE)


if __name__ == "__main__":
    main()
