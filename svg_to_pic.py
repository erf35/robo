#import pydobot as bot
#from serial.tools import list_ports
import os
import time
import math
import svgpathtools
import pydobot as bot
from serial.tools import list_ports

def safe_move_to(device, target_x, target_y, target_z, target_r, wait=True):
    for attempt in range(5):
        try:
            device.move_to(target_x, target_y, target_z, target_r, wait)
            return
        except AttributeError as e:
            if "params" in str(e):
                print(f"Warning: Communication error during move_to, checking connection... ({attempt + 1}/5)")
                time.sleep(0.5)
            else:
                raise

step = 0.5
def svg_to_points(svg_path, step=step, decimals=2):
    """
    Converts an SVG file into a list of (x, y) points.
    
    Args:
        svg_path: Path to the SVG file
        step: Distance between points (lower = more detailed)
        decimals: Number of decimal places for output coordinates
        
    Returns:
        List of (x, y) lists/tuples
    """
    paths, attributes = svgpathtools.svg2paths(svg_path)
    points = []
    
    for path in paths:
        length = path.length()
        if length == 0:
            continue
        path_points = []
            
        num_steps = int(length / step)
        if num_steps == 0:
            num_steps = 1
            
        for i in range(num_steps + 1):
            t = i / num_steps
            point = path.point(t)
            path_points.append([
                round(point.real, decimals),
                round(point.imag, decimals)
            ])
        points.append(path_points)
            
    return points

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')

device = None

if available_ports:
    port = available_ports[1].device
    device = bot.Dobot(port=port, verbose=True)
    pozice = device.pose()
    x = pozice[0]
    y = pozice[1]
    z = pozice[2]
    r = pozice[3]
else:
    print('No robot connected. Printing points only.')
    x = 0.0
    y = 0.0
    z = 0.0
    r = 0.0


script_dir = os.path.dirname(os.path.abspath(__file__))
svg_file = os.path.join(script_dir, 'clvek.svg')
points = svg_to_points(svg_file)

draw_z = -63
travel_z = draw_z + 20
vertical_change_threshold = step * 1.5  # Threshold for deciding when to lift the pen
previous_point = None

for path_points in points:
    if not path_points:
        continue

    for point in path_points:
        point_x = float(point[0])
        point_y = float(point[1])

        if previous_point is None:
            movement_length = 0.0
            needs_vertical_change = False
        else:
            movement_length = math.sqrt((point_x - previous_point[0]) ** 2 + (point_y - previous_point[1]) ** 2)
            needs_vertical_change = movement_length > vertical_change_threshold

        if device:
            if previous_point is not None and needs_vertical_change:
                # Lift before long XY travel, then move and lower at destination.
                safe_move_to(device, x+previous_point[0], y+previous_point[1], travel_z, r, True)
                safe_move_to(device, x+point_x, y+point_y, travel_z, r, True)
                safe_move_to(device, x+point_x, y+point_y, draw_z, r, True)
            else:
                safe_move_to(device, x+point_x, y+point_y, draw_z, r, True)

        print(
            f'{point_x} {point_y} movement_xy={movement_length:.3f} '
            f'vertical_change={"YES" if needs_vertical_change else "NO"}'
        )
        previous_point = (point_x, point_y)

if device:
    device.close()