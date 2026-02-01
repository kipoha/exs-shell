import sys
from exs_shell.app import App


def main():
    if len(sys.argv) == 1:
        App.run()
    elif len(sys.argv) == 2 and sys.argv[1] == "--debug":
        App.run(debug=True)
    else:
        print("Unknown command")
        exit(1)


if __name__ == "__main__":
    main()
