import argparse

from exs_shell.cli.shell import shell_cmd
from exs_shell.cli.ipc import ipc_cmd
from exs_shell.cli.update import update_cmd
from exs_shell.cli.version import version_cmd


def main():
    parser = argparse.ArgumentParser(prog="exs", description="EXS Shell CLI")

    sub = parser.add_subparsers(dest="command", required=True)

    shell = sub.add_parser("shell", help="Shell commands")
    shell_cmd(shell)

    ipc = sub.add_parser("ipc", help="IPC commands", add_help=False)
    ipc_cmd(ipc)

    sub.add_parser("update", help="Update EXS(not implemented)").set_defaults(
        func=update_cmd
    )
    sub.add_parser("version", help="Show version").set_defaults(func=version_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
