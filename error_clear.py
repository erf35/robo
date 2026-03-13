import argparse
from typing import Optional, Set

import serial
from serial.tools import list_ports

from pydobot_message import Message


class DobotException(Exception):
	pass


def _find_dobot_port() -> str:
	for port in list_ports.comports():
		if port.vid in (4292, 6790):
			return port.device
	raise DobotException("Dobot device not found")


class DobotAlarmCleaner:
	def __init__(self, port: Optional[str] = None, baudrate: int = 115200) -> None:
		if port is None:
			port = _find_dobot_port()

		try:
			self._ser = serial.Serial(
				port=port,
				baudrate=baudrate,
				parity=serial.PARITY_NONE,
				stopbits=serial.STOPBITS_ONE,
				bytesize=serial.EIGHTBITS,
				timeout=0.3,
			)
		except serial.serialutil.SerialException as exc:
			raise DobotException(f"Cannot open serial port {port}: {exc}") from exc

	def close(self) -> None:
		if self._ser.is_open:
			self._ser.close()

	def __enter__(self) -> "DobotAlarmCleaner":
		return self

	def __exit__(self, exc_type, exc, tb) -> None:
		self.close()

	def _send_command(self, msg: Message) -> Message:
		self._ser.reset_input_buffer()
		self._ser.write(msg.bytes())
		response = self._read_message()
		if response is None:
			raise DobotException("No response from Dobot")
		return response

	def _read_message(self) -> Optional[Message]:
		begin_found = False
		last_byte = None
		tries = 64

		while not begin_found and tries > 0:
			raw = self._ser.read(1)
			if not raw:
				tries -= 1
				continue
			current_byte = raw[0]
			if current_byte == 0xAA and last_byte == 0xAA:
				begin_found = True
			last_byte = current_byte
			tries -= 1

		if not begin_found:
			return None

		payload_len_raw = self._ser.read(1)
		if not payload_len_raw:
			return None
		payload_len = payload_len_raw[0]

		payload_and_checksum = self._ser.read(payload_len + 1)
		if len(payload_and_checksum) != payload_len + 1:
			return None

		data = bytearray([0xAA, 0xAA, payload_len])
		data.extend(payload_and_checksum)
		return Message(data)

	def get_alarms(self) -> Set[int]:
		msg = Message()
		msg.id = 20
		response = self._send_command(msg)

		alarms: Set[int] = set()
		for byte_idx in range(min(16, len(response.params))):
			alarm_byte = response.params[byte_idx]
			for bit in range(8):
				if alarm_byte & (1 << bit):
					alarms.add(byte_idx * 8 + bit)
		return alarms

	def clear_alarms(self) -> None:
		msg = Message()
		msg.id = 20
		msg.ctrl = 0x01
		self._send_command(msg)


def main() -> int:
	parser = argparse.ArgumentParser(description="Read and clear Dobot alarms")
	parser.add_argument("--port", default=None, help="Serial port, for example COM4")
	parser.add_argument("--baudrate", default=115200, type=int, help="Serial baudrate")
	parser.add_argument(
		"--no-clear",
		action="store_true",
		help="Only read alarms, do not clear them",
	)
	args = parser.parse_args()

	try:
		with DobotAlarmCleaner(port=args.port, baudrate=args.baudrate) as cleaner:
			before = sorted(cleaner.get_alarms())
			print(f"Active alarms before: {before if before else 'none'}")

			if not args.no_clear:
				cleaner.clear_alarms()
				after = sorted(cleaner.get_alarms())
				print(f"Active alarms after:  {after if after else 'none'}")
		return 0
	except DobotException as exc:
		print(f"Error: {exc}")
		return 1


if __name__ == "__main__":
	raise SystemExit(main())
