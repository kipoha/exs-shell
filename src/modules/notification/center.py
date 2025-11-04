from ignis import widgets, utils
from ignis.services.notifications import Notification, NotificationService

from gi.repository import GLib  # type: ignore

from base.singleton import SingletonClass
from base.window.animated import PartiallyAnimatedWindow

from config import config
from config.user import options

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


class NotificationCenter(PartiallyAnimatedWindow, SingletonClass):
    def __init__(self, **kwargs):
        self.dnd_button = widgets.Button(
            child=widgets.Label(label=""),
            on_click=lambda x: self.toggle_dnd(),
            css_classes=["notification-dnd"],
        )

        self.clear_button = widgets.Button(
            child=widgets.Label(label="󰩹"),
            on_click=lambda x: notifications.clear_all(),
            css_classes=["notification-clear-all"],
        )

        self.header_buttons = widgets.Box(
            css_classes=["notification-center-header-buttons"],
            halign="end",
            hexpand=True,
            child=[self.dnd_button, self.clear_button],
            spacing=5,
        )

        self.left_corner = widgets.Corner(
            css_classes=["notification-left-corner"],
            orientation="bottom-right",
            width_request=50,
            height_request=70, 
            halign="end",
            valign="end", 
        )
        self.right_corner = widgets.Corner(
            css_classes=["notification-right-corner"],
            orientation="bottom-left",
            width_request=50,
            height_request=70, 
            halign="end",
            valign="end",
        )

        self._box = widgets.Box(
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

        self._main_box = widgets.Box(
            css_classes=["notification-center"],
            child=[self.left_corner, self._box, self.right_corner]
        )

        self._animated_parts = [self.left_corner, self.right_corner, self._box]

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

        self.update_dnd_button()

        options.notifications.bind("dnd", lambda *_: self.update_dnd_button())

    def toggle_dnd(self):
        options.notifications.set_dnd(not options.notifications.dnd)
        self.update_dnd_button()

    def update_dnd_button(self):
        css = self.dnd_button.get_style_context()
        if options.notifications.dnd:
            css.add_class("active")
        else:
            css.remove_class("active")
