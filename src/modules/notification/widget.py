import asyncio

from ignis import widgets, utils
from ignis.window_manager import WindowManager
from ignis.services.notifications import Notification, NotificationService

from config import config


notifications = NotificationService.get_default()
window_manager = WindowManager.get_default()


class ScreenshotLayout(widgets.Box):
    def __init__(self, notification: Notification) -> None:
        super().__init__(
            vertical=True,
            hexpand=True,
            child=[
                widgets.Box(
                    child=[
                        widgets.Picture(
                            image=notification.icon,
                            content_fit="cover",
                            width=1920 // 7,
                            height=1080 // 7,
                            style="border-radius: 1rem; background-color: black;",
                        ),
                        widgets.Button(
                            child=widgets.Icon(
                                image="window-close-symbolic", pixel_size=20
                            ),
                            halign="end",
                            valign="start",
                            hexpand=True,
                            css_classes=["notification-close"],
                            on_click=lambda x: notification.close(),
                        ),
                    ],
                ),
                widgets.Label(
                    label="Screenshot saved",
                    css_classes=["notification-screenshot-label"],
                ),
                widgets.Box(
                    homogeneous=True,
                    style="margin-top: 0.75rem;",
                    spacing=10,
                    child=[
                        widgets.Button(
                            child=widgets.Label(label="Open"),
                            css_classes=["notification-action"],
                            on_click=lambda x: asyncio.create_task(
                                utils.exec_sh_async(f"xdg-open {notification.icon}")
                            ),
                        ),
                        widgets.Button(
                            child=widgets.Label(label="Close"),
                            css_classes=["notification-action"],
                            on_click=lambda x: notification.close(),
                        ),
                    ],
                ),
            ],
        )


class NormalLayout(widgets.Box):
    def __init__(self, notification: Notification) -> None:
        super().__init__(
            vertical=True,
            hexpand=True,
            child=[
                widgets.Box(
                    child=[
                        widgets.Icon(
                            image=notification.icon
                            if notification.icon
                            else "dialog-information-symbolic",
                            pixel_size=48,
                            halign="start",
                            valign="start",
                        ),
                        widgets.Box(
                            vertical=True,
                            style="margin-left: 0.75rem;",
                            child=[
                                widgets.Label(
                                    ellipsize="end",
                                    label=notification.summary,
                                    halign="start",
                                    visible=notification.summary != "",
                                    css_classes=["notification-summary"],
                                ),
                                widgets.Label(
                                    label=notification.body,
                                    ellipsize="end",
                                    halign="start",
                                    css_classes=["notification-body"],
                                    visible=notification.body != "",
                                ),
                            ],
                        ),
                        widgets.Button(
                            child=widgets.Icon(
                                image="window-close-symbolic", pixel_size=20
                            ),
                            halign="end",
                            valign="start",
                            hexpand=True,
                            css_classes=["notification-close"],
                            on_click=lambda x: notification.close(),
                        ),
                    ],
                ),
                widgets.Box(
                    child=[
                        widgets.Button(
                            child=widgets.Label(label=action.label),
                            on_click=lambda x, action=action: action.invoke(),
                            css_classes=["notification-action"],
                        )
                        for action in notification.actions
                    ],
                    homogeneous=True,
                    style="margin-top: 0.75rem;" if notification.actions else "",
                    spacing=10,
                ),
            ],
        )


class NotificationWidget(widgets.Box):
    def __init__(self, notification: Notification) -> None:
        layout: NormalLayout | ScreenshotLayout

        if notification.app_name == "grimblast":
            layout = ScreenshotLayout(notification)
        else:
            layout = NormalLayout(notification)

        super().__init__(
            css_classes=["notification"],
            child=[layout],
        )


class Popup(widgets.Box):
    def __init__(
        self, box: "PopupBox", window: "NotificationPopup", notification: Notification
    ):
        self._box = box
        self._window = window

        widget = NotificationWidget(notification)
        widget.css_classes = ["notification-popup"]

        self._inner = widgets.Revealer(transition_type="slide_left", child=widget)
        self._outer = widgets.Revealer(transition_type="slide_down", child=self._inner)
        super().__init__(child=[self._outer], halign="end")

        notification.connect("dismissed", lambda x: self.destroy())

    def destroy(self):
        def box_destroy():
            self.unparent()
            if len(notifications.popups) == 0:
                self._window.visible = False

        def outer_close():
            self._outer.reveal_child = False
            utils.Timeout(self._outer.transition_duration, box_destroy)

        self._inner.transition_type = "crossfade"
        self._inner.reveal_child = False
        utils.Timeout(self._outer.transition_duration, outer_close)


class PopupBox(widgets.Box):
    def __init__(self, window: "NotificationPopup", monitor: int):
        self._window = window
        self._monitor = monitor

        super().__init__(
            vertical=True,
            valign="start",
            setup=lambda self: notifications.connect(
                "new_popup",
                lambda x, notification: self.__on_notified(notification),
            ),
        )

    def __on_notified(self, notification: Notification) -> None:
        lockscreen = window_manager.get_window(f"{config.NAMESPACE}_lockscreen")
        if not lockscreen.visible:
            self._window.visible = True
            popup = Popup(box=self, window=self._window, notification=notification)
            self.prepend(popup)
            popup._outer.reveal_child = True
            utils.Timeout(
                popup._outer.transition_duration, popup._inner.set_reveal_child, True
            )


class NotificationPopup(widgets.Window):
    def __init__(self, monitor_id: int):
        super().__init__(
            anchor=["right", "top", "bottom"],
            monitor=monitor_id,
            namespace=f"{config.NAMESPACE}_notification_popup_{monitor_id}",
            layer="top",
            child=PopupBox(window=self, monitor=monitor_id),
            visible=False,
            dynamic_input_region=True,
            css_classes=["notification-popup-window"],
            style="min-width: 29rem;",
        )
