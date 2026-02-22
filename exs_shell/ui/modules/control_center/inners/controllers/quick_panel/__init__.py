from typing import Any

from ignis.widgets import Box, Grid

from exs_shell.ui.modules.control_center.inners.controllers.quick_panel.powerprofile import (
    PowerProfile,
)
from exs_shell.ui.modules.control_center.inners.controllers.quick_panel.bluetooth import (
    BluetoothWidget,
)
from exs_shell.ui.modules.control_center.inners.controllers.quick_panel.wifi import (
    WifiWidget,
)
from exs_shell.ui.modules.control_center.inners.controllers.quick_panel.dark import (
    DarkTheme,
)


class QuickPanel(Box):
    def __init__(self, scale: float = 1.0, **kwargs: Any):
        self.scale = scale

        self.system = Box(
            vertical=True,
            css_classes=["control-center-quick-panel-system"],
            child=[
                PowerProfile(scale=self.scale),
                DarkTheme(scale=self.scale),
            ],
            hexpand=True,
            spacing=5 * self.scale,
            halign="fill",
        )
        self.network = Box(
            vertical=True,
            css_classes=["control-center-quick-panel-network"],
            child=[
                WifiWidget(scale=self.scale),
                BluetoothWidget(scale=self.scale),
            ],
            hexpand=True,
            spacing=5 * self.scale,
            halign="fill",
        )
        self._box = Box(
            css_classes=["control-center-quick-panel"],
            child=[self.network, self.system],
            hexpand=True,
            spacing=5 * self.scale,
            halign="fill",
        )
        super().__init__(child=[self._box], hexpand=True, halign="fill", **kwargs)
