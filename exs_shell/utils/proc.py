import os
import traceback
import psutil
import signal
import ctypes
from loguru import logger


def kill_process():
    parent = psutil.Process(os.getpid())
    for child in parent.children(recursive=True):
        try:
            if child.status() == psutil.STATUS_ZOMBIE:
                child.terminate()
                try:
                    child.wait(timeout=1)
                except psutil.TimeoutExpired:
                    child.kill()
                    child.wait(timeout=1)
        except Exception:
            logger.error(traceback.format_exc())
            pass


def set_death_signal():
    libc = ctypes.CDLL("libc.so.6")
    libc.prctl(1, signal.SIGTERM)
