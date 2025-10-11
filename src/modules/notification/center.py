from ignis import widgets, utils
from ignis.services.notifications import Notification, NotificationService

from gi.repository import GLib  # type: ignore

from base.singleton import SingletonClass
from base.window.animated import AnimatedWindow
from config import config

from modules.notification.widget import NotificationWidget


notifications = NotificationService.get_default()


class Popup(widgets.Revealer):
    def __init__(self, notification: Notification, **kwargs):
        widget = NotificationWidget(notification)
        super().__init__(child=widget, transition_type="slide_down", **kwargs)

        notification.connect("closed", lambda x: self.destroy())

    def destroy(self):
        self.reveal_child = False
        utils.Timeout(self.transition_duration, self.unparent)


class NotificationList(widgets.Box):
    __gtype_name__ = "NotificationList"

    def __init__(self):
        loading_notifications_label = widgets.Label(
            label="Loading notifications...",
            valign="center",
            vexpand=True,
            css_classes=["notification-center-info-label"],
        )

        super().__init__(
            vertical=True,
            child=[loading_notifications_label],
            vexpand=True,
            css_classes=["rec-unset"],
            setup=lambda self: notifications.connect(
                "notified",
                lambda x, notification: self.__on_notified(notification),
            ),
        )

        utils.ThreadTask(
            self.__load_notifications,
            lambda result: self.set_child(result),
        ).run()

    def __on_notified(self, notification: Notification) -> None:
        notify = Popup(notification)
        self.prepend(notify)
        notify.reveal_child = True

    def __load_notifications(self) -> list[widgets.Label | Popup]:
        contents: list[widgets.Label | Popup] = []
        for i in notifications.notifications:
            GLib.idle_add(lambda i=i: contents.append(Popup(i, reveal_child=True)))

        contents.append(
            widgets.Label(
                label="No notifications",
                valign="center",
                vexpand=True,
                visible=notifications.bind(
                    "notifications", lambda value: len(value) == 0
                ),
                css_classes=["notification-center-info-label"],
            )
        )
        return contents


class NotificationCenter(AnimatedWindow, SingletonClass):
    def __init__(self, **kwargs):
        self.header_buttons = widgets.Box(
            css_classes=["notification-center-header-buttons"],
            halign="end",
            hexpand=True,
            child=[
                widgets.Button(
                    child=widgets.Label(label=""),
                    on_click=lambda x: self.dnd(),  # not working
                    css_classes=["notification-dnd"],
                ),
                widgets.Button(
                    child=widgets.Label(label="󰩹"),
                    on_click=lambda x: notifications.clear_all(),
                    css_classes=["notification-clear-all"],
                ),
            ],
            spacing=5,
        )
        self._main_box = widgets.Box(
            vertical=True,
            css_classes=["notification-center-window", "hidden"],
            child=[
                widgets.Box(
                    css_classes=["notification-center-header"],
                    child=[
                        widgets.Label(
                            label=notifications.bind(
                                "notifications", lambda value: str(len(value))
                            ),
                            css_classes=["notification-count"],
                        ),
                        widgets.Label(
                            label="notifications",
                            css_classes=["notification-header-label"],
                        ),
                        self.header_buttons,
                    ],
                ),
                widgets.Scroll(
                    child=NotificationList(),
                    vexpand=True,
                ),
            ],
        )

        super().__init__(
            namespace=f"{config.NAMESPACE}_notification",
            anchor=["bottom"],
            default_width=600,
            default_height=400,
            resizable=False,
            visible=False,
            child=self._main_box,
            **kwargs,
        )

    def dnd(self):
        raise NotImplementedError("DND not implemented")
