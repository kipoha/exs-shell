from ignis import widgets
from exs_shell.window.settings.elements.row import SettingsRow


class FileRow(SettingsRow):
    def __init__(
        self,
        dialog: widgets.FileDialog,
        button_label: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._button = widgets.FileChooserButton(
            dialog=dialog,
            label=widgets.Label(
                label=button_label, ellipsize="start", max_width_chars=20
            ),
            hexpand=True,
            halign="end",
            css_classes=["settings-row-file-button"],
        )

        self.child.append(self._button)
