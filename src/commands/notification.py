from ignis.command_manager import CommandManager


command_manager = CommandManager.get_default()


def generate_notification_commands(notification) -> None:
    @command_manager.command("toggle-notification-center")
    def toggle_notification_center(*_):
        notification.toggle()
