from ignis import widgets
from window.settings.elements import SettingsRow

class DividerRow(SettingsRow):
    def __init__(self, **kwargs):
        super().__init__(label=None, sublabel=None, css_classes=[], **kwargs)
        for child in list(self.child):
            self.child.remove(child)

        separator = widgets.Separator(
            vertical=False,
            hexpand=True,
            css_classes=["settings-row-separator"],
        )
        self.child.append(separator)
