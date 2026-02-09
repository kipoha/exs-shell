from ignis.widgets import Box, Picture, Button, Icon, Label
from ignis.services.notifications import Notification
from ignis.utils import exec_sh_async

from exs_shell.utils.loop import run_async_task


class ScreenshotLayout(Box):
    def __init__(self, notification: Notification) -> None:
        super().__init__(
            vertical=True,
            hexpand=True,
            child=[
                Box(
                    child=[
                        Picture(
                            image=notification.icon,
                            content_fit="cover",
                            width=1920 // 7,
                            height=1080 // 7,
                            style="border-radius: 1rem; background-color: black;",
                            can_focus=False,
                            focusable=False,
                        ),
                        Button(
                            child=Icon(image="window-close-symbolic", pixel_size=20),
                            halign="end",
                            valign="start",
                            hexpand=True,
                            css_classes=["notification-close"],
                            on_click=lambda x: notification.close(),
                            can_focus=False,
                            focusable=False,
                        ),
                    ],
                ),
                Label(
                    label="Screenshot saved",
                    css_classes=["notification-screenshot-label"],
                ),
                Box(
                    homogeneous=True,
                    style="margin-top: 0.75rem;",
                    spacing=10,
                    child=[
                        Button(
                            child=Label(label="Open"),
                            css_classes=["notification-action"],
                            on_click=lambda x: run_async_task(
                                exec_sh_async(f"xdg-open {notification.icon}")
                            ),
                            can_focus=False,
                            focusable=False,
                        ),
                        Button(
                            child=Label(label="Close"),
                            css_classes=["notification-action"],
                            on_click=lambda x: notification.close(),
                            can_focus=False,
                            focusable=False,
                        ),
                    ],
                ),
            ],
        )


class NormalLayout(Box):
    def __init__(self, notification: Notification) -> None:
        super().__init__(
            vertical=True,
            hexpand=True,
            child=[
                Box(
                    child=[
                        Icon(
                            image=notification.icon
                            if notification.icon
                            else "dialog-information-symbolic",
                            pixel_size=48,
                            halign="start",
                            valign="start",
                        ),
                        Box(
                            vertical=True,
                            style="margin-left: 0.75rem;",
                            child=[
                                Label(
                                    ellipsize="end",
                                    label=notification.summary,
                                    halign="start",
                                    visible=notification.summary != "",
                                    css_classes=["notification-summary"],
                                ),
                                Label(
                                    label=notification.body,
                                    ellipsize="end",
                                    halign="start",
                                    css_classes=["notification-body"],
                                    visible=notification.body != "",
                                ),
                            ],
                        ),
                        Button(
                            child=Icon(image="window-close-symbolic", pixel_size=20),
                            halign="end",
                            valign="start",
                            hexpand=True,
                            css_classes=["notification-close"],
                            on_click=lambda x: notification.close(),
                            can_focus=False,
                            focusable=False,
                        ),
                    ],
                ),
                Box(
                    child=[
                        Button(
                            child=Label(label=action.label),
                            on_click=lambda x, action=action: action.invoke(),
                            css_classes=["notification-action"],
                            can_focus=False,
                            focusable=False,
                        )
                        for action in notification.actions
                    ],
                    homogeneous=True,
                    style="margin-top: 0.75rem;" if notification.actions else "",
                    spacing=10,
                ),
            ],
        )


class NotificationWidget(Box):
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
