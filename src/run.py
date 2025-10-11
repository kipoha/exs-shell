import os
import sys


sys.path.insert(0, os.path.dirname(__file__))


from config import config as App
from pathlib import Path

BASE_DIR = Path(__file__).parent

cfg = str(BASE_DIR / "main.py")


def main():
    if len(sys.argv) == 1:
        App(cfg)
    else:
        print("unknown command")
        exit(1)


if __name__ == "__main__":
    main()
