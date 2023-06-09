from herbstluftwm import monitors_info, Geometry
from subprocess import Popen
from typing import Literal
from util import setup_logger, spawn
import argparse
import logging
import signal
import time

"""
Constants
___
"""

BORDER_W = 1
HEIGHT   = 40
PADDING  = 16

"""
Main
___
"""
logger = logging.getLogger(__name__)

LogLevel = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

def add_arguments(argparser: argparse.ArgumentParser):
    argparser.add_argument(
        '-l', '--logfile', dest='logfile', default='lemoney.log'
    )
    argparser.add_argument(
        '--level', dest='loglevel', default='DEBUG',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set logging level'
    )
    argparser.add_argument(
        '-m', '--monitors', dest='monitors', default=None, type=int, nargs='+',
        help='Select which monitors to render on. If omitted render on all monitors'
    )

def calculate_bar_geometry(geometry: Geometry):
    """Calculate bar geometry with border"""

    width = geometry['width'] - PADDING * 2 - BORDER_W * 2
    height = HEIGHT - BORDER_W * 2 - BORDER_W * 2
    border_width  = width + BORDER_W * 2
    border_height = height + BORDER_W * 2

    x = geometry['x'] + PADDING + BORDER_W
    y = PADDING + BORDER_W
    border_x = geometry['x'] + PADDING
    border_y = PADDING

    return f'{width}x{height}+{x}+{y}', f'{border_width}x{border_height}+{border_x}+{border_y}'

def cleanup(procs: list[Popen[str]]):
    for proc in procs:
        proc.kill()

def handler(signum, frame):
    logger.info(frame.f_lineno)
    signame = signal.Signals(signum).name if signum is not None else 'UNKNOWN'
    raise Exception(f'Received signal {signame} @ lineno {frame.f_lineno}')

signal.signal(signal.SIGTERM, handler)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        prog='Lemoney',
        description='Control lemonbar'
    )

    add_arguments(argparser)

    args = argparser.parse_args()

    loglevel_arg: LogLevel = args.loglevel

    match loglevel_arg:
        case 'DEBUG':    loglevel = logging.DEBUG
        case 'INFO':     loglevel = logging.INFO
        case 'WARNING':  loglevel = logging.WARNING
        case 'ERROR':    loglevel = logging.ERROR
        case 'CRITICAL': loglevel = logging.CRITICAL

    setup_logger(loglevel, args.logfile)

    filter_monitors = args.monitors is not None
    procs: list[Popen[str]] = []

    for index, geometry in monitors_info():
        if filter_monitors and index not in args.monitors: # Skip filtered monitors
            continue

        top_bar_geometry, top_border_geometry = calculate_bar_geometry(geometry)

        lemonbar_cmd = f'lemonbar -n Lemoney -g {top_bar_geometry}'

        procs.append(spawn(lemonbar_cmd, check=True, text=True))

    counter = 0

    try:
        while True:
            for proc in procs:
                if proc.stdin is not None:
                    print(f'{counter}', file=proc.stdin, flush=True)
            counter += 1
    except:
        logger.exception('Exception in main loop!')
        raise
    finally:
        cleanup(procs)

