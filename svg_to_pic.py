#import pydobot as bot
#from serial.tools import list_ports
import os
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

port = available_ports[1].device

device = bot.Dobot(port=port, verbose=True)
pozice = device.pose()
x = pozice[0]
y = pozice[1]
z = pozice[2]
r = pozice[3]


script_dir = os.path.dirname(os.path.abspath(__file__))
svg_file = os.path.join(script_dir, 'a.svg')  # Replace with your SVG file name
points = svg_to_points(svg_file)

draw_z = -50
travel_z = draw_z + 20

for path_points in points:
    if not path_points:
        continue

    # Lift the tool before moving to a disconnected path.
    start_point = path_points[0]
    device.move_to(x+float(start_point[0]), y+float(start_point[1]), travel_z, r, True)
    device.move_to(x+float(start_point[0]), y+float(start_point[1]), draw_z, r, True)
    print(float(start_point[0]), float(start_point[1]))

    for point in path_points[1:]:
        device.move_to(x+float(point[0]), y+float(point[1]), draw_z, r, True)
        print(float(point[0]), float(point[1]))

device.close()