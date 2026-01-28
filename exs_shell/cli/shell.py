import sys
from exs_shell.app import App
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

cfg = str(BASE_DIR / "init.py")


def main():
    if len(sys.argv) == 1:
        App.run(cfg)
    elif len(sys.argv) == 2 and sys.argv[1] == "--debug":
        App.run(cfg, debug=True)
    else:
        print("Unknown command")
        exit(1)


if __name__ == "__main__":
    main()
