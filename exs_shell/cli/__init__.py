import argparse

from exs_shell.cli import ipc, plugin, shell, version


def main():
    parser = argparse.ArgumentParser(prog="exs", description="EXS Shell CLI")

    sub = parser.add_subparsers(dest="command", required=True)

    shell_ = sub.add_parser("shell", help="Shell commands")
    shell.cmd(shell_)

    ipc_ = sub.add_parser("ipc", help="IPC commands", add_help=False)
    ipc.cmd(ipc_)

    sub.add_parser("version", help="Show version").set_defaults(func=version.cmd)

    plugin_ = sub.add_parser("plugin", help="Plugin commands")
    plugin.cmd(plugin_)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
