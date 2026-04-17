import json
from pathlib import Path
from typing import Any, Dict, List, Sequence

from serial.tools import list_ports

import pydobotplus as bot


def _extract_xyzr(raw_pose: Any) -> List[float]:
    if hasattr(raw_pose, "position"):
        values = raw_pose.position
        return [float(values[0]), float(values[1]), float(values[2]), float(values[3])]

    if isinstance(raw_pose, (list, tuple)) and len(raw_pose) >= 4:
        return [float(raw_pose[0]), float(raw_pose[1]), float(raw_pose[2]), float(raw_pose[3])]

    raise ValueError("Unsupported pose format. Expected object with .position or tuple/list with 4 values.")


def _read_pose_from_device(device: Any) -> List[float]:
    if hasattr(device, "get_pose") and callable(device.get_pose):
        return _extract_xyzr(device.get_pose())
    if hasattr(device, "pose") and callable(device.pose):
        return _extract_xyzr(device.pose())
    if hasattr(device, "get_position") and callable(device.get_position):
        return _extract_xyzr(device.get_position())

    raise ValueError("Device does not provide get_pose(), pose(), or get_position()")


def create_positions(
    count: int,
    names: List[str],
    device: Any,
) -> Dict[str, List[float]]:
    """
    Capture robot positions interactively.

    Args:
        count: Number of positions to capture.
        names: Position names.
        device: Robot device object with get_pose(), pose(), or get_position().

    Returns:
        Dict in form: {"name": [x, y, z, r]}
    """
    if count < 1:
        raise ValueError("count must be at least 1")
    if len(names) < count:
        raise ValueError("names list must contain at least count items")

    positions: Dict[str, List[float]] = {}

    for i in range(count):
        name = names[i]

        print(f'Position for "{name}"')
        input("Press Enter to write this position...")
        pose = _read_pose_from_device(device)

        positions[name] = pose
        print(f"Saved {name}: {positions[name]}")

    return positions


def capture_and_save_positions(
    names: Sequence[str],
    device: Any,
    file_path: str = "positions.json",
) -> Dict[str, List[float]]:
    positions = create_positions(count=len(names), names=list(names), device=device)
    save_positions(positions, file_path)
    return positions


def create_positions_file(
    names: Sequence[str],
    device: Any,
    file_path: str = "positions.json",
) -> Dict[str, List[float]]:
    return capture_and_save_positions(names=names, device=device, file_path=file_path)


def capture_positions_to_file(
    position_names: Sequence[str],
    device: Any,
    position_file: str = "positions.json",
) -> Dict[str, List[float]]:


    try:
        positions = create_positions_file(
            names=position_names,
            device=device,
            file_path=position_file,
        )
        print(f"Saved positions to {position_file}")
        return positions
    finally:
        device.close()


def save_positions(positions: Dict[str, List[float]], file_path: str = "positions.json") -> None:
    path = Path(file_path)
    with path.open("w", encoding="utf-8") as file:
        json.dump(positions, file, indent=2)


def load_positions(file_path: str = "positions.json") -> Dict[str, List[float]]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Position file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Invalid positions data format. Expected a dictionary.")

    normalized: Dict[str, List[float]] = {}
    for name, values in data.items():
        if not isinstance(values, list) or len(values) < 4:
            raise ValueError(f"Invalid pose for '{name}'. Expected [x, y, z, r].")
        normalized[name] = [float(values[0]), float(values[1]), float(values[2]), float(values[3])]

    return normalized


def get_positions_from_file(file_path: str = "positions.json") -> Dict[str, List[float]]:
    return load_positions(file_path)
