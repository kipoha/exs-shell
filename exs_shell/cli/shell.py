import argparse
from exs_shell.app import App


def shell_cmd(parser: argparse.ArgumentParser):
    parser.add_argument("--dev", action="store_true", help="Run the app in development mode")
    parser.add_argument("--debug", action="store_true", help="Run the app in debug mode")
    parser.add_argument("--reload", action="store_true", help="Run the app in reload mode")

    parser.set_defaults(func=run_shell)


def run_shell(args: argparse.Namespace):
    App.run(debug=args.debug, dev=args.dev, reload=args.reload)
