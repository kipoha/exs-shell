import os
import psutil
import signal
import ctypes


kill_process_names = ["cava", "bwrap"]


def kill_process():
    parent = psutil.Process(os.getpid())
    for child in parent.children(recursive=True):
        try:
            name = child.name()
            if name in kill_process_names:
                child.terminate()
                try:
                    child.wait(timeout=1)
                except psutil.TimeoutExpired:
                    child.kill()
                    child.wait(timeout=1)
        except Exception:
            pass


def set_death_signal():
    libc = ctypes.CDLL("libc.so.6")
    libc.prctl(1, signal.SIGTERM)
