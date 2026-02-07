import sys
import argparse
from exs_shell.app import App


def main():
    parser = argparse.ArgumentParser(description="Run the EXS Shell App")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run the app in debug mode"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Run the app in development mode"
    )

    args = parser.parse_args()

    App.run(debug=args.debug, dev=args.dev)


if __name__ == "__main__":
    main()
