from ignis.command_manager import CommandManager


command_manager = CommandManager.get_default()


def generate_launcher_commands(launcher) -> None:
    @command_manager.command("toggle-launcher")
    def toggle_launcher(*_):
        launcher.toggle()
