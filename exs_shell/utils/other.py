from exs_shell.utils.path import Paths, Dirs


class ShellCommandBuilder:
    @staticmethod
    def matugen(image_path: str, scheme: str, dark: bool, *args: str) -> str:
        config_file = Dirs.CONFIG_DIR / "exs-shell" / "matugen" / "config.toml"
        if not config_file.exists():
            config_file = Paths.root / "matugen" / "config.toml"
        mode = "dark" if dark else "light"
        other_param = " ".join(args)
        return (
            f"matugen image -c '{config_file}' -t scheme-{scheme} '{image_path}' -m '{mode}'"
            + " "
            + other_param
        )


SCB: type[ShellCommandBuilder] = ShellCommandBuilder
