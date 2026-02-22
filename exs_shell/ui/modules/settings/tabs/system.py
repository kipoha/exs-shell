import ignis
from ignis.widgets import Picture, Separator
from ignis.services.fetch import FetchService

import exs_shell
from exs_shell.state import State
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
)


class SoftwareCategory(BaseCategory):
    def __init__(self):
        self.fetch: FetchService = State.services.fetch
        super().__init__(
            child=[
                CategoryLabel(title="Software", icon=Icons.ui.SYSTEM),
                SettingsRow(
                    title="Operating System",
                    description=self.fetch.os_name,
                    child=[
                        Picture(
                            image=self.fetch.os_logo
                            or self.fetch.os_logo_dark
                            or "unknown",
                            width=30,
                            height=30,
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    title="Kernel",
                    description=self.fetch.kernel,
                ),
                Separator(),
                SettingsRow(
                    title="Desktop Environment",
                    description=self.fetch.current_desktop,
                ),
                Separator(),
                SettingsRow(
                    title="Hostname",
                    description=self.fetch.hostname.strip(),
                ),
                Separator(),
                SettingsRow(
                    title="BIOS version",
                    description=self.fetch.bios_version,
                ),
                Separator(),
                SettingsRow(
                    title="Exs Shell version",
                    description=exs_shell.__version__,
                ),
                Separator(),
                SettingsRow(
                    title="Ignis version",
                    description=ignis.__version__,
                ),
            ]
        )


class AppearanceCategory(BaseCategory):
    def __init__(self):
        self.fetch: FetchService = State.services.fetch
        super().__init__(
            child=[
                CategoryLabel(title="Appearance", icon=Icons.ui.PALLETTE),
                SettingsRow(
                    title="GTK Theme",
                    description=self.fetch.gtk_theme,
                ),
                Separator(),
                SettingsRow(
                    title="Icon Theme",
                    description=self.fetch.icon_theme,
                ),
            ]
        )


class HardwareCategory(BaseCategory):
    def __init__(self):
        self.fetch: FetchService = State.services.fetch
        super().__init__(
            child=[
                CategoryLabel(title="Hardware", icon=Icons.ui.DESKTOP),
                SettingsRow(
                    title="CPU",
                    description=self.fetch.cpu,
                ),
                Separator(),
                SettingsRow(
                    title="RAM",
                    description=(str(round(self.fetch.mem_total / 1024 / 1024, 2)) + " GiB"),
                ),
                Separator(),
                SettingsRow(
                    title="GPU",
                    description="N/A",
                ),
            ]
        )


class SystemTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                SoftwareCategory(),
                AppearanceCategory(),
                HardwareCategory(),
            ]
        )
