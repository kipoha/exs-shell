from typing import Any

from ignis import utils
from ignis.services.notifications import Notification, NotificationService
from ignis.widgets import Box, Label

from gi.repository import GLib  # type: ignore

from exs_shell import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.state import State
from exs_shell.ui.modules.notification.shared import NotificationWidget
from exs_shell.ui.widgets.windows import Revealer


@register.event
class Popup(Revealer):
    def __init__(self, notification: Notification, **kwargs: Any):
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
