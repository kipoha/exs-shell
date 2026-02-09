from typing import Any

from ignis import utils
from ignis.services.notifications import Notification, NotificationService
from ignis.widgets import Box, Button, CenterBox, Corner, Label, Scroll

from gi.repository import GLib  # type: ignore

from exs_shell import register
from exs_shell.configs.user import notifications
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.gtk.windows import KeyboardMode
from exs_shell.state import State
from exs_shell.ui.factory import window
from exs_shell.ui.modules.notification.shared import NotificationWidget
from exs_shell.ui.widgets.base import MonitorRevealerBaseWidget
from exs_shell.ui.widgets.windows import Revealer


@register.event
class Popup(Revealer):
    def __init__(self, notification: Notification, **kwargs):
        self.notification = notification
        widget = NotificationWidget(notification)
        super().__init__(
            child=widget, transition_type=RevealerTransition.SLIDE_DOWN, **kwargs
        )

    @register.events.notifications("closed", True)
    def destroy(self, *_):
        self.reveal_child = False
        utils.Timeout(self.transition_duration, self.unparent)


@register.event
class NotificationList(Box):
    __gtype_name__ = "NotificationList"

    def __init__(self):
        loading_notifications_label = Label(
            label="Loading notifications...",
            valign="center",
            vexpand=True,
            css_classes=["notification-center-info-label"],
        )
        self.notifications: NotificationService = State.services.notifications

        super().__init__(
            vertical=True,
            child=[loading_notifications_label],
            vexpand=True,
            css_classes=["rec-unset"],
        )

        utils.ThreadTask(
            self.__load_notifications,
            lambda result: self.set_child(result),
        ).run()

    @register.events.notifications("notified")
    def __on_notified(self, _, notification: Notification) -> None:
        notify = Popup(notification)
        self.prepend(notify)
        notify.reveal_child = True

    def __load_notifications(self) -> list[Label | Popup]:  # type: ignore
        contents: list[Label | Popup] = []  # type: ignore
        for i in self.notifications.notifications:
            GLib.idle_add(lambda i=i: contents.append(Popup(i, reveal_child=True)))

        contents.append(
            Label(
                label="No notifications",
                valign="center",
                vexpand=True,
                visible=self.notifications.bind(
                    "notifications", lambda value: len(value) == 0
                ),
                css_classes=["notification-center-info-label"],
            )
        )
        return contents


@register.event
@register.window
@register.commands
class NotificationCenter(MonitorRevealerBaseWidget):
    def __init__(
        self,
        transition_type: RevealerTransition = RevealerTransition.SLIDE_RIGHT,
        transition_duration: int = 400,
        reveal_child: bool = False,
    ) -> None:
        self.notifications: NotificationService = State.services.notifications
        self.widget_build()
        win = window.create(
            "notification_center",
            # anchor=["bottom", "right", "top"],
            anchor=["top", "bottom", "right"],
            kb_mode=KeyboardMode.ON_DEMAND,
            visible=False,
            popup=True,
        )
        super().__init__(
            self._box, win, transition_type, transition_duration, reveal_child
        )
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
            css_classes=["notification-left-corner"],
            orientation="top-right",
            width_request=50,
            height_request=70,
            halign="end",
            valign="end",
        )
        self.bottom_corner = Corner(
            css_classes=["notification-right-corner"],
            orientation="bottom-right",
            width_request=50,
            height_request=70,
            halign="end",
            valign="end",
        )

        self._inner = Box(
            vertical=True,
            css_classes=["notification-center-window", "hidden"],
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
        )
        self.corners = CenterBox(
            css_classes=["notification-center-corners"],
            vertical=True,
            start_widget=self.top_corner,
            end_widget=self.bottom_corner,
            # child=[self.top_corner, Box(vexpand=True), self.bottom_corner],
        )

        self._box = Box(
            css_classes=["notification-center"],
            child=[self.corners, self._inner],
        )

    @register.command(group="notificationCenter", description="Clear all notifications", name="clear")
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

    @register.command(group="notificationCenter", description="Toggle notification center")
    def toggle(self):
        self.set_visible(not self.visible)
