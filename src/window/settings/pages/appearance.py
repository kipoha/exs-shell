from ignis import widgets
from window.settings.elements import (
    SettingsPage,
    SettingsGroup,
    SettingsEntry,
    FileRow,
)

from config.user import options


class AppearanceEntry(SettingsEntry):
    def __init__(self):
        self.file_dialog = widgets.FileDialog(
            initial_path=options.wallpaper.wallpaper_dir,
            on_file_set=lambda _, file: options.wallpaper.set_wallpaper_path(
                file.get_path()
            ),
        )
        self.folder_dialog = widgets.FileDialog(
            initial_path=options.wallpaper.wallpaper_dir,
            select_folder=True,
            on_file_set=lambda _, file: options.wallpaper.set_wallpaper_dir(
                file.get_path()
            ),
        )

        page = SettingsPage(
            name="Appearance",
            groups=[
                SettingsGroup(
                    name="General",
                    rows=[
                        FileRow(
                            label="Wallpaper",
                            sublabel="Wallpaper directory",
                            dialog=self.folder_dialog,
                            button_label="Choose Folder",
                        ),
                        FileRow(
                            label="Wallpaper",
                            sublabel="Wallpaper path",
                            button_label="Choose File",
                            dialog=self.file_dialog,
                        ),
                    ],
                )
            ],
        )
        super().__init__(
            label="Appearance",
            icon="󰏘",
            page=page,
        )
        options.wallpaper.connect_option("wallpaper_dir", self.update_dialog)

    def update_dialog(self):
        self.file_dialog.initial_path = options.wallpaper.wallpaper_dir  # type: ignore
        self.folder_dialog.initial_path = options.wallpaper.wallpaper_dir  # type: ignore
