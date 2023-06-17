from typing import IO
import logging
import shlex
import subprocess

logger = logging.getLogger(__name__)

def setup_logger(level: int | None = logging.DEBUG, log_filename: str | None = None):
    logging.basicConfig(
        filename=log_filename,
        filemode='a',
        format='%(asctime)s | %(levelname)s | %(name)s | %(pathname)s | %(processName)s : %(message)s',
        datefmt='%H:%M:%S',
        level=level
    )

def get_output(cmd: str, check: bool = True, timeout: float | None = None, text: bool = True) -> str:
    try:
        proc = subprocess.run(shlex.split(cmd), capture_output=True, check=check, timeout=timeout, text=text)
        return proc.stdout.strip()
    except subprocess.CalledProcessError as error:
        logger.error(error.stderr.strip())
        if check:
            raise error
        return error.stdout.strip()

def spawn(cmd: str, check: bool = False, *args, **kwargs):
    try:
        proc = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, *args, **kwargs)
    except FileNotFoundError as error:
        logger.error(f'spawn failed: cmd not found: {error.filename}')
        raise
    return_code = proc.poll()
    if return_code is not None and return_code != 0:
        stdout, stderr = proc.communicate()
        logger.debug(stdout)
        logger.error(stderr)
        if check:
            raise subprocess.CalledProcessError(cmd=cmd, returncode=return_code, output=stdout, stderr=stderr)
    return proc

def write_at_0(fs: IO[str], data: str, flush = True):
    fs.seek(0)
    fs.write(data + '\n')
    if flush:
        fs.flush()

def readline_at_0(fs: IO[str]):
    fs.seek(0)
    return fs.readline().strip()

