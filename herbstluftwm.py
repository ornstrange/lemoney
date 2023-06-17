from typing import Literal
from util import *
import logging
import shutil

HC = shutil.which('herbstclient')

logger = logging.getLogger(__name__)

GeometryKey = Literal['width', 'height', 'x', 'y']
Geometry = dict[GeometryKey, int]

def parse_geometry(geometry: str) -> Geometry:
    width_height, _, offsets = geometry.partition('+')
    width, height = width_height.split('x')
    x, y = offsets.split('+')
    return {
        'width':  int(width),
        'height': int(height),
        'x':      int(x),
        'y':      int(y)
    }

def monitors_info(filter_monitors: list[int] = []):
    get_monitors_cmd = f'{HC} list_monitors'
    get_monitors_output = get_output(get_monitors_cmd)

    for monitor_output in get_monitors_output.split('\n'):
        index = int(monitor_output[0])
        geometry = parse_geometry(monitor_output[3:].split(' ')[0])
        if filter_monitors and index not in filter_monitors:
            continue
        yield index, geometry

if __name__ == '__main__':
    print(list(monitors_info()))

