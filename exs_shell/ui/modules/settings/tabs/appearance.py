import os
from threading import Thread

from gi.repository import GLib  # type: ignore

from ignis.widgets import (
    Box,
    Button,
    FileFilter,
    Grid,
    Label,
    Overlay,
    Picture,
    Scroll,
    Separator,
)

from exs_shell import register
from exs_shell.configs.user import appearance
from exs_shell.interfaces.enums.colorschemes import ColorSchemes
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    FileDialogRow,
    SpinRow,
    SwitchRow,
)


class WallpaperCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel("Wallpaper", Icons.ui.IMAGE),
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
            button_name=Icons.ui.IMAGE_OFF,
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
        file_chooser_button.remove_css_class("settings-row-dialog-button")

        wallpaper_icon = Box(
            valign="fill",
            halign="fill",
            css_classes=["settings-wallpaper-icon"],
            child=[
                Label(
                    label=Icons.ui.IMAGE,
                    halign="center",
                    valign="center",
                    css_classes=["settings-wallpaper-icon-label"],
                )
            ],
            can_target=False,
        )

        wallpaper_overlay = Overlay(
            css_classes=["settings-wallpaper-overlay"],
            child=self.wallpaper_picture,
        )

        wallpaper_overlay.add_overlay(self.wallpaper_filename_label)
        wallpaper_overlay.add_overlay(wallpaper_icon)
        wallpaper_overlay.add_overlay(file_chooser_button)

        self.append(wallpaper_overlay)

    def _set_and_update_wallpaper(self, path: str | None):
        if path:
            appearance.wallpaper_path = path
            self.wallpaper_picture.set_image(path)
            self.wallpaper_filename_label.label = os.path.basename(path)


class ThemeCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel("Theme", Icons.ui.PALLETTE),
                SettingsRow(
                    title="Color Scheme",
                    description="Change color scheme",
                    vertical=True,
                    child=[
                        Box(
                            css_classes=["settings-row-palette"],
                            halign="fill",
                            valign="center",
                            spacing=10,
                            child=[
                                Button(
                                    css_classes=[
                                        "settings-row-palette-button",
                                        "active"
                                        if scheme.value
                                        == appearance.scheme
                                        else "",
                                    ],
                                    on_click=lambda _, s=scheme: self.on_palette_change(
                                        _, s
                                    ),
                                    child=Box(
                                        css_classes=[
                                            "settings-row-palette-button-colors",
                                            scheme.name.lower(),
                                        ],
                                        vertical=True,
                                        height_request=50,
                                        width_request=50,
                                        halign="center",
                                        hexpand=False,
                                        valign="center",
                                        vexpand=False,
                                        tooltip_text=scheme.name.capitalize(),
                                        child=[
                                            Box(
                                                css_classes=["primary"],
                                                height_request=25,
                                                width_request=50,
                                                hexpand=False,
                                                halign="start",
                                            ),
                                            Box(
                                                vertical=False,
                                                child=[
                                                    Box(
                                                        css_classes=["secondary"],
                                                        height_request=25,
                                                        width_request=25,
                                                    ),
                                                    Box(
                                                        css_classes=["tertiary"],
                                                        height_request=25,
                                                        width_request=25,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                )
                                for scheme in ColorSchemes
                            ],
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    title="Contrast",
                    description="Edit contrast theme",
                    child=[
                        SpinRow(
                            min=-1,
                            max=1,
                            value=appearance.bind("contrast"),
                            on_change=lambda active: appearance.set_contrast(active),
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    title="Dark",
                    description="Enable dark theme",
                    child=[
                        SwitchRow(
                            active=appearance.bind("dark"),
                            on_change=lambda active: appearance.set_dark(active),
                        )
                    ],
                ),
            ],
        )

    def on_palette_change(self, _, scheme: ColorSchemes):
        appearance.set_scheme(scheme.value)
        buttons = self.get_child()[1].get_child()[1]
        for button in buttons:
            button.remove_css_class("active")
        _.add_css_class("active")


@register.event
class WallpaperQuickControl(BaseCategory):
    def __init__(self, w: WallpaperCategory):
        self.w = w
        self.gallery_content_container = Box(
            vertical=True,
            halign="fill",
            hexpand=True,
            valign="fill",
            vexpand=True,
            css_classes=["settings-wallpaper-gallery-container"],
        )
        loading_label = Label(label="Loading wallpapers...")
        self.gallery_content_container.append(loading_label)
        super().__init__(
            child=[
                CategoryLabel("Select", Icons.ui.IMAGE_OFF),
                SettingsRow(
                    title="Wallpaper Folder",
                    description="Change wallpaper folder",
                    child=[
                        FileDialogRow(
                            lambda _, path: appearance.set_wallpaper_dir(
                                path.get_path()
                            ),
                            initial_path=appearance.bind("wallpaper_dir"),
                            select_folder=True,
                        )
                    ],
                ),
                Separator(),
                self.gallery_content_container,
            ],
        )
        self._find_and_create_gallery_async()

    @register.events.option(appearance, "wallpaper_dir")
    def _update_gallery(self):
        self.gallery_content_container.set_child([])
        self._find_and_create_gallery_async()

    def _find_and_create_gallery_async(self):
        def do_find_and_build():
            wallpaper_dir = appearance.wallpaper_dir
            if not wallpaper_dir or not os.path.isdir(
                os.path.expanduser(wallpaper_dir)
            ):
                wallpaper_dir = os.path.expanduser("~/Pictures/Wallpapers")

            if not os.path.isdir(wallpaper_dir):
                GLib.idle_add(self._replace_gallery_content, None)
                return

            supported_extensions = (".png", ".jpg", ".jpeg", ".gif")
            image_files = []
            try:
                with os.scandir(wallpaper_dir) as entries:
                    for entry in entries:
                        if entry.is_file() and entry.name.lower().endswith(
                            supported_extensions
                        ):
                            image_files.append(entry.path)
            except Exception:
                GLib.idle_add(self._replace_gallery_content, None)
                return

            image_files.sort()
            if not image_files:
                GLib.idle_add(self._replace_gallery_content, None)
                return

            gallery_grid = Grid(
                halign="fill",
                hexpand=True,
                column_spacing=5,
                row_spacing=5,
            )
            columns = 4
            temp_thumbnails = []
            current_path = appearance.wallpaper_path

            for idx, file_path in enumerate(image_files):
                is_selected = file_path == current_path
                btn = Button(
                    on_click=lambda _, path=file_path: (
                        self.w._set_and_update_wallpaper(path),
                        self._update_selected_icons(),
                    ),
                    child=Picture(
                        image=file_path,
                        content_fit="cover",
                        height=100,
                        width=196,
                        hexpand=True,
                        halign="fill",
                        css_classes=["settings-wallpaper-thumbnail-image"]
                        + (["active"] if is_selected else []),
                    ),
                    hexpand=True,
                    halign="fill",
                    css_classes=["settings-wallpaper-thumbnail"]
                    + (["active"] if is_selected else []),
                )
                btn.wallpaper_path = file_path
                gallery_grid.attach(btn, idx % columns, idx // columns, 1, 1)
                temp_thumbnails.append(btn)

            gallery_scroll = Scroll(
                width_request=600,
                height_request=300,
            )
            gallery_scroll.set_child(gallery_grid)
            GLib.idle_add(
                self._replace_gallery_content, gallery_scroll, temp_thumbnails
            )

        loader_thread = Thread(target=do_find_and_build)
        loader_thread.daemon = True
        loader_thread.start()

    def _update_selected_icons(self):
        current_path = appearance.wallpaper_path
        for btn in self.thumbnail_overlays:
            if btn.wallpaper_path == current_path:
                btn.add_css_class("active")
                btn.get_child().add_css_class("active")
            else:
                btn.remove_css_class("active")
                btn.get_child().remove_css_class("active")

    def _replace_gallery_content(self, new_child, thumbnail_buttons=None):
        while self.gallery_content_container.get_last_child():
            self.gallery_content_container.remove(
                self.gallery_content_container.get_last_child()
            )

        if new_child:
            self.gallery_content_container.append(new_child)
            if thumbnail_buttons is not None:
                self.thumbnail_overlays = thumbnail_buttons
        else:
            self.gallery_content_container.append(
                Label(
                    label="No wallpapers found in the directory.",
                    css_classes=["message"],
                )
            )


class AppearanceTab(BaseTab):
    def __init__(self):
        w = WallpaperCategory()
        super().__init__(
            child=[
                w,
                ThemeCategory(),
                WallpaperQuickControl(w),
            ]
        )
