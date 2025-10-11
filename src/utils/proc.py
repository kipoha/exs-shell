import os
import psutil


def kill_process():
    parent = psutil.Process(os.getpid())
    for child in parent.children(recursive=True):
        try:
            child.terminate()
            try:
                child.wait(timeout=1)
            except psutil.TimeoutExpired:
                child.kill()
                child.wait(timeout=1)
        except Exception:
            pass
