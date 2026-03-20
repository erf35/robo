#import pydobot as bot
#from serial.tools import list_ports
import os
import svgpathtools
import pydobot as bot
from serial.tools import list_ports

def svg_to_points(svg_path, step=10, decimals=2):
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
            
        num_steps = int(length / step)
        if num_steps == 0:
            num_steps = 1
            
        for i in range(num_steps + 1):
            t = i / num_steps
            point = path.point(t)
            points.append([
                round(point.real, decimals),
                round(point.imag, decimals)
            ])
            
    return float(points)

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
svg_file = os.path.join(script_dir, 'a.svg')
points = svg_to_points(svg_file)


for point in points:
    device.move_to(x+float(point[0]), y+float(point[1]), -50, r, True)
    delay = 0.1  # Adjust this delay as needed
    print(point[0], point[1])

device.close()