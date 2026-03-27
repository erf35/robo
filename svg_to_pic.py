#import pydobot as bot
#from serial.tools import list_ports
import os
import math
import svgpathtools
import pydobot as bot
from serial.tools import list_ports

def svg_to_points(svg_path, step=1, decimals=2):
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
svg_file = os.path.join(script_dir, 'a.svg')  # Replace with your SVG file name
points = svg_to_points(svg_file)

draw_z = -60
travel_z = draw_z + 20
vertical_change_threshold = 1.5
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
                device.move_to(x+previous_point[0], y+previous_point[1], travel_z, r, True)
                device.move_to(x+point_x, y+point_y, travel_z, r, True)
                device.move_to(x+point_x, y+point_y, draw_z, r, True)
            else:
                device.move_to(x+point_x, y+point_y, draw_z, r, True)

        print(
            f'{point_x} {point_y} movement_xy={movement_length:.3f} '
            f'vertical_change={"YES" if needs_vertical_change else "NO"}'
        )
        previous_point = (point_x, point_y)

if device:
    device.close()