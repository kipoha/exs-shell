import argparse

from exs_shell.utils import plugin


def cmd(parser: argparse.ArgumentParser):
    plugin_sub = parser.add_subparsers(dest="plugin_cmd")

    plugin_sub.add_parser("list", help="List plugins")

    add_ = plugin_sub.add_parser("add", help="Add plugin")
    add_.add_argument("name", help="Plugin name")

    remove_ = plugin_sub.add_parser("remove", help="Remove plugin")
    remove_.add_argument("name", help="Plugin name")

    new_ = plugin_sub.add_parser("new", help="Create and init new plugin")
    new_.add_argument("name", help="Plugin name")

    parser.set_defaults(func=run_plugin, plugin_parser=parser)


def run_plugin(args: argparse.Namespace):
    cmd_: str = args.plugin_cmd
    match cmd_:
        case "add":
            plugin.install(args.name)
        case "remove":
            plugin.remove(args.name)
        case "list":
            plugin.list()
        case "new":
            plugin.new(args.name)
        case _:
            args.plugin_parser.print_help()
