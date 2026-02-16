import os
from ignis.widgets import FileFilter, Label, Overlay, Picture, Separator

from exs_shell.configs.user import appearance
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    FileDialogRow,
    SwitchRow,
)


class WallpaperCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel("Wallpaper", "image"),
            ],
        )

        self.wallpaper_picture = Picture(
            height=300,
            width=560,
            vexpand=False,
            hexpand=False,
            content_fit="cover",
            css_classes=["settings-wallpaper-preview"],
            image=appearance.bind("wallpaper_path"),
        )

        self.wallpaper_filename_label = Label(
            label=os.path.basename(appearance.wallpaper_path or "")
            or "Click to set wallpaper",
            halign="start",
            valign="end",
            margin_start=10,
            margin_bottom=10,
            css_classes=["settings-wallpaper-filename-label"],
        )

        def on_file_set_handler(_, file):
            path = file.get_path()
            self._set_and_update_wallpaper(path)

        file_chooser_button = FileDialogRow(
            on_file_set_handler,
            button_name="",
            css_classes=["settings-wallpaper-button-overlay"],
            initial_path=appearance.wallpaper_path,
            filters=[
                FileFilter(
                    mime_types=[
                        "image/jpeg",
                        "image/png",
                        "image/webp",
                        "image/gif",
                    ],
                    default=True,
                    name="Images (PNG, JPG, WebP, GIF)",
                )
            ],
        )

        wallpaper_overlay = Overlay(
            css_classes=["settings-wallpaper-overlay"],
            child=self.wallpaper_picture,
        )

        wallpaper_overlay.add_overlay(file_chooser_button)
        wallpaper_overlay.add_overlay(self.wallpaper_filename_label)

        self.append(wallpaper_overlay)

    def _set_and_update_wallpaper(self, path: str | None):
        if path:
            appearance.wallpaper_path = path
            self.wallpaper_picture.set_image(path)
            self.wallpaper_filename_label.label = os.path.basename(path)


class AppearanceTab(BaseTab):
    def __init__(self):
        super().__init__(child=[
            WallpaperCategory(),
        ])
