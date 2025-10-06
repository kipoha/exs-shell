from ignis.command_manager import CommandManager



command_manager = CommandManager.get_default()


def generate_osd_commands(osd) -> None:
    @command_manager.command("volume-up")
    def volume_up(*_):
        osd.update_volume(up=True)

    @command_manager.command("volume-down")
    def volume_down(*_):
        osd.update_volume(up=False)

    @command_manager.command("volume-mute")
    def toggle_mute(*_):
        osd.toggle_mute()

    @command_manager.command("brightness-up")
    def brightness_up(*_):
        osd.update_brightness(up=True)

    @command_manager.command("brightness-down")
    def brightness_down(*_):
        osd.update_brightness(up=False)
