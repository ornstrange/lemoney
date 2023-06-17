from herbstluftwm import Geometry
from settings import *
from typing import NotRequired, TypedDict
import shutil

def calculate_border_bar_geometry(geometry: Geometry, border_width: int = 1):
    """Calculate border bar geometry"""

    width = geometry['width'] - PADDING * 2
    height = HEIGHT

    x = geometry['x'] + PADDING
    y = PADDING
    return f'{width}x{height}+{x}+{y}'

def calculate_bar_geometry(geometry: Geometry, border_width: int = 1):
    """Calculate bar geometry"""

    width = geometry['width'] - PADDING * 2 - border_width * 2
    height = HEIGHT - border_width * 2

    x = geometry['x'] + PADDING + border_width
    y = PADDING + border_width

    return f'{width}x{height}+{x}+{y}'

Options = TypedDict('Options', {
    'background': NotRequired[str],
    'bottom':     NotRequired[bool],
    'font':       NotRequired[str],
    'font_bold':  NotRequired[str],
    'foreground': NotRequired[str],
    'geometry':   NotRequired[str],
    'name':       NotRequired[str],
})

def generate_lemonbar_cmd(options: Options = {}):
    formats = {
        'name':       ' -n {}',
        'bottom':     ' -b',
        'geometry':   ' -g {}',
        'font':       ' -f {}',
        'font_bold':  ' -f {}',
        'foreground': ' -F {}',
        'background': ' -B {}'
    }
    defaults = {
        'name': 'Lemoney',
        'font': FONT,
        'font_bold': FONT_BOLD,
    }

    cmd = shutil.which('lemonbar') or 'lemonbar'

    # Loop formats dict to ensure order of font and font_bold, and always use the same order of options.
    for option, format_str in formats.items():
        value = options.get(option, defaults.get(option))
        cmd += format_str.format(value) if value else ''
    return cmd

