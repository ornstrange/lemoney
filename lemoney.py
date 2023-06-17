from config import read_config
from herbstluftwm import monitors_info
from lemonbar import *
from settings import HEIGHT, PADDING
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
        '-k', '--kill', dest='kill', action='store_true'
    )
    argparser.add_argument(
        '-l', '--logfile', dest='logfile', default='lemoney.log'
    )
    argparser.add_argument(
        '--conf', dest='config', default='lemoney.yaml'
    )
    argparser.add_argument(
        '--level', dest='loglevel', default='DEBUG',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set logging level'
    )
    argparser.add_argument(
        '-m', '--monitors', dest='monitors', default=[], type=int, nargs='+', metavar='MONITOR',
        help='Select which monitors to render on. If omitted render on all monitors',
    )
    argparser.add_argument(
        '-f', '--foreground', dest='foreground', default='#ffffff', type=str,
        help='Foreground color: #aarrggbb, #rrggbb or #rgb', metavar='COLOR'
    )
    argparser.add_argument(
        '-b', '--background', dest='background', default='#000000', type=str,
        help='Background color: #aarrggbb, #rrggbb or #rgb', metavar='COLOR'
    )
    argparser.add_argument(
        '-bc', '--bordercolor', dest='border_color', default='#ffffff', type=str,
        help='Border color: #aarrggbb, #rrggbb or #rgb', metavar='COLOR'
    )
    argparser.add_argument(
        '-bw', '--borderwidth', dest='border_width', default=1, type=int,
        help='Border color: #aarrggbb, #rrggbb or #rgb', metavar='WIDTH'
    )

def cleanup(procs: list[Popen[str]] | dict[str, list[Popen[str]]]):
    if type(procs) == dict:
        for proc in procs['top'] + procs['bot']:
            proc.kill()
        return
    assert type(procs) == list
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

    if args.kill:
        pids = get_output("pgrep -f 'python.*lemoney.py'", check=False)
        for pid in pids.split('\n'):
            get_output(f'kill {pid}')
        exit(0)

    config = read_config(args.config)

    border_procs: list[Popen[str]] = []
    procs: dict[str, list[Popen[str]]] = { 'top': [], 'bot': [] }

    top = True
    bot = False

    # Start border "bars"
    for index, geometry in monitors_info(args.monitors):
        border_geometry = calculate_border_bar_geometry(geometry, args.border_width)

        if top:
            border_procs.append(spawn_bar(
                border_geometry,
                f'{index}-top-border',
                {
                    'background': args.border_color
                }
            ))
        if bot:
            border_procs.append(spawn_bar(
                border_geometry,
                f'{index}-bot-border',
                {
                    'bottom':     True,
                    'background': args.border_color
                }
            ))

    # Start bars
    for index, geometry in monitors_info(args.monitors):
        geometry = calculate_bar_geometry(geometry, args.border_width)

        if top:
            procs['top'].append(spawn_bar(
                geometry,
                f'{index}-top-border',
                {
                    'background': args.background,
                    'foreground': args.foreground
                }
            ))
        if bot:
            procs['bot'].append(spawn_bar(
                geometry,
                f'{index}-bot-border',
                {
                    'bottom':     True,
                    'background': args.background,
                    'foreground': args.foreground
                }
            ))

    # Set padding for herbstluftwm
    for index, geometry in monitors_info(args.monitors):
        pad_cmd = f'herbstclient pad {index}'
        pad_cmd += f' {HEIGHT + PADDING} 0' if top else ' 0 0'
        pad_cmd += f' {HEIGHT + PADDING} 0' if bot else ' 0 0'
        get_output(pad_cmd)

    counter = 0

    # Main loop
    import time
    from formatting import right, left
    slept = 0
    battery = get_output('sh /home/ornstrange/.config/scripts/batt2.sh')
    try:
        while True:
            if slept % 120 == 119:
                battery = get_output('sh /home/ornstrange/.config/scripts/batt2.sh')
            date = get_output('date "+%c"')
            for proc in procs['top']:
                if proc.stdin is not None:
                    print(f'{left("  " + battery)}{right(date + "  ")}', file=proc.stdin, flush=True)
            # for proc in procs['bot']:
            #     if proc.stdin is not None:
            #         print(f' BOT {counter}', file=proc.stdin, flush=True)
            # counter += 1
            time.sleep(1)
            slept += 1
    except:
        logger.exception('Exception in main loop!')
    finally:
        cleanup(border_procs)
        cleanup(procs)

