from typing import Any

from ignis.services.notifications import NotificationService
from ignis.widgets import Box, Button, CenterBox, Corner, Label, Scroll

from exs_shell import register
from exs_shell.configs.user import notifications
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.gtk.windows import KeyboardMode
from exs_shell.state import State
from exs_shell.ui.factory import window
from exs_shell.ui.modules.control_center.inners.notification import NotificationList
from exs_shell.ui.widgets.base import MonitorRevealerBaseWidget
from exs_shell.ui.widgets.windows import Revealer
from exs_shell.ui.modules.control_center.inners.controllers.mpris.controller import MprisController
from exs_shell.ui.modules.control_center.inners.controllers.mpris.mini import MiniPlayer


@register.event
@register.window
@register.commands
class ControlCenter(MonitorRevealerBaseWidget):
    def __init__(
        self,
    ) -> None:
        self.notifications: NotificationService = State.services.notifications
        self.widget_build()
        win = window.create(
            "notification_center",
            anchor=["top", "bottom", "right"],
            kb_mode=KeyboardMode.NONE,
            visible=False,
            popup=True,
            dynamic_input_region=True,
        )
        super().__init__(self._box, win, [self._rev_corners, self._rev_inner])
        self._inner.set_size_request(400 * self.scale, -1)

    def widget_build(self) -> None:
        self.dnd_button = Button(
            child=Label(label=""),
            on_click=self.toggle_dnd,
            css_classes=["notification-dnd"],
            can_focus=False,
            focusable=False,
        )
        self.clear_button = Button(
            child=Label(label="󰩹"),
            on_click=self.clear_all,
            css_classes=["notification-clear-all"],
        )

        self.header_buttons = Box(
            css_classes=["notification-center-header-buttons"],
            halign="end",
            hexpand=True,
            spacing=5,
            child=[self.dnd_button, self.clear_button],
        )

        self.top_corner = Corner(
            css_classes=["control-corner"],
            orientation="top-right",
            width_request=30,
            height_request=30,
            halign="end",
            valign="end",
        )
        self.bottom_corner = Corner(
            css_classes=["control-corner"],
            orientation="bottom-right",
            width_request=30,
            height_request=30,
            halign="end",
            valign="end",
        )
        self._notifications = Box(
            vertical=True,
            child=[
                Box(
                    css_classes=["notification-center-header"],
                    child=[
                        Label(
                            label=self.notifications.bind(
                                "notifications", lambda value: str(len(value))
                            ),
                            css_classes=["notification-count"],
                        ),
                        Label(
                            label="notifications",
                            css_classes=["notification-header-label"],
                        ),
                        self.header_buttons,
                    ],
                ),
                Scroll(
                    child=NotificationList(),
                    vexpand=True,
                ),
            ],
            css_classes=["notification-list"],
            vexpand=True,
        )
        self._inner = Box(
            vertical=True,
            child=[self._notifications, MprisController()],
            vexpand=True,
            css_classes=["control-center-window"],
        )

        self.corners = CenterBox(
            vertical=True,
            vexpand=False,
            hexpand=False,
            start_widget=self.top_corner,
            end_widget=self.bottom_corner,
        )

        self._rev_corners = Revealer(
            transition_type=RevealerTransition.SLIDE_LEFT,
            transition_duration=300,
            child=self.corners,
        )
        self._rev_inner = Revealer(
            transition_type=RevealerTransition.SLIDE_LEFT,
            transition_duration=200,
            child=self._inner,
            vexpand=True,
        )
        self._box = Box(
            css_classes=["notification-center"],
            child=[self._rev_corners, self._rev_inner],
            vexpand=True,
        )

    @register.command(
        group="notification", description="Clear all notifications", name="clear"
    )
    def clear_all(self, *_: Any):
        self.notifications.clear_all()

    def toggle_dnd(self, *_: Any):
        notifications.set_dnd(not notifications.dnd)
        self.update_dnd_button()

    @register.events.option(notifications, "dnd")
    def update_dnd_button(self):
        css = self.dnd_button.get_style_context()
        if notifications.dnd:
            css.add_class("active")
        else:
            css.remove_class("active")

    @register.command(group="controlCenter", description="Toggle the control center")
    def toggle(self):
        self.set_visible(not self.visible)
