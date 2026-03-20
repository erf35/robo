#import pydobot as bot
#from serial.tools import list_ports
import os
import svgpathtools
import pydobot as bot
from serial.tools import list_ports

def svg_to_points(svg_path, step=10):
    """
    Converts an SVG file into a list of (x, y) points.
    
    Args:
        svg_path: Path to the SVG file
        step: Distance between points (lower = more detailed)
        
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
            points.append([point.real, point.imag])
            
    return points

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[1].device

device = bot.Dobot(port=port, verbose=True)


script_dir = os.path.dirname(os.path.abspath(__file__))
svg_file = os.path.join(script_dir, 'a.svg')
points = svg_to_points(svg_file)

print(points)