from exs_shell.utils.path import Paths, Dirs


class ShellCommandBuilder:
    @staticmethod
    def matugen(image_path: str, scheme: str, dark: bool, contrast: int, *args: str) -> str:
        config_file = Dirs.CONFIG_DIR / "exs-shell" / "matugen" / "config.toml"
        if not config_file.exists():
            config_file = Paths.path / "matugen" / "config.toml"
        print(config_file)
        mode = "dark" if dark else "light"
        other_param = " ".join(args)
        return (
            f"matugen image -c '{config_file}' -t scheme-{scheme} '{image_path}' -m '{mode}' --contrast {contrast}"
            + " "
            + other_param
        )

    @staticmethod
    def gsettings(dark: bool) -> str:
        mode = "dark" if dark else "light"
        return f"gsettings set org.gnome.desktop.interface color-scheme 'prefer-{mode}'"


SCB: type[ShellCommandBuilder] = ShellCommandBuilder
