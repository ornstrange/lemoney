from formatting import background
from herbstluftwm import monitors_info
from lemonbar import *
from settings import BORDER_W, HEIGHT, PADDING
from subprocess import Popen
from typing import Literal
from util import get_output, setup_logger, spawn
import argparse
import logging
import signal

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
        '-m', '--monitors', dest='monitors', default=[], type=int, nargs='+',
        help='Select which monitors to render on. If omitted render on all monitors'
    )

def cleanup(procs: list[Popen[str]]):
    for proc in procs:
        proc.kill()

def handler(signum, frame):
    logger.info(frame.f_lineno)
    signame = signal.Signals(signum).name if signum is not None else 'UNKNOWN'
    raise Exception(f'Received signal {signame} @ lineno {frame.f_lineno}')

signal.signal(signal.SIGTERM, handler)

def spawn_bar(geometry, suffix='', options={}):
    lemonbar_cmd = generate_lemonbar_cmd({ 'name': f'Lemoney-{suffix}', 'geometry': geometry, **options })
    return spawn(lemonbar_cmd, check=True, text=True)

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

    border_procs: list[Popen[str]] = []
    procs: list[Popen[str]] = []

    top = True
    bot = True

    # Start border "bars"
    for index, geometry in monitors_info(args.monitors):
        border_geometry = calculate_border_bar_geometry(geometry)

        if top:
            border_procs.append(spawn_bar(border_geometry, f'{index}-top-border', { 'background': '#ffffff' }))
        if bot:
            border_procs.append(spawn_bar(border_geometry, f'{index}-bot-border', { 'bottom': True, 'background': '#ffffff' }))

    # Start bars
    for index, geometry in monitors_info(args.monitors):
        geometry = calculate_bar_geometry(geometry)

        if top:
            procs.append(spawn_bar(geometry, f'{index}-top'))
        if bot:
            procs.append(spawn_bar(geometry, f'{index}-bot', { 'bottom': True }))

    # Set padding for herbstluftwm
    for index, geometry in monitors_info(args.monitors):
        pad_cmd = f'herbstclient pad {index}'
        pad_cmd += f' {HEIGHT + PADDING} 0' if top else ' 0 0'
        pad_cmd += f' {HEIGHT + PADDING} 0' if bot else ' 0 0'
        get_output(pad_cmd)

    counter = 0

    # Main loop
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

