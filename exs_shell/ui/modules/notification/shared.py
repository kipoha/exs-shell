import time

from urllib.parse import unquote, urlparse

from pathlib import Path

from gi.repository import GLib  # type: ignore

from ignis.widgets import Box, Picture, Button, Label, Scale
from ignis.services.notifications import Notification
from ignis.utils import exec_sh_async

from exs_shell.ui.widgets.custom.icon import Icon
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.utils.loop import run_async_task
from exs_shell.configs.user import notifications


def _start_timeout(_: Notification, scale: Scale, timeout: int):
    start_time = time.monotonic()
    duration = timeout / 1000

    def update():
        elapsed = time.monotonic() - start_time
        progress = 100 - (elapsed / duration) * 100
        scale.set_value(progress)
        return True

    GLib.timeout_add(16, update)


class ScreenshotLayout(Box):
    def __init__(
        self,
        notification: Notification,
        popup: bool = False,
        timeout: int = notifications.popup_timeout,
    ) -> None:
        if "file:/" in notification.icon:
            uri = notification.icon
            path = Path(unquote(urlparse(uri).path))
        else:
            path = notification.icon
        self._scale = Scale(
            vertical=False,
            min=0,
            max=100,
            step=1,
            value=100,
            draw_value=False,
            sensitive=False,
            css_classes=["notification-progress"],
        )
        childs = []
        if popup:
            childs.append(self._scale)
        base = [
            Box(
                child=[
                    Picture(
                        image=str(path),
                        content_fit="cover",
                        width=1920 // 5,
                        height=1080 // 5,
                        can_focus=False,
                        focusable=False,
                        css_classes=["notification-screenshot"],
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
        ]
        childs.extend(base)
        super().__init__(
            vertical=True,
            hexpand=True,
            child=childs,
        )
        if popup and timeout > 0:
            _start_timeout(notification, self._scale, timeout)


class NormalLayout(Box):
    def __init__(
        self,
        notification: Notification,
        popup: bool = False,
        timeout: int = notifications.popup_timeout,
    ) -> None:
        self._scale = Scale(
            vertical=False,
            min=0,
            max=100,
            step=1,
            value=100,
            draw_value=False,
            sensitive=False,
            css_classes=["notification-progress"],
        )
        childs = []
        if popup:
            childs.append(self._scale)
        base = [
            Box(
                child=[
                    Picture(
                        image=notification.icon
                        if notification.icon
                        else "dialog-information-symbolic",
                        width=48,
                        height=48,
                        content_fit="cover",
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
                        child=Icon(label=Icons.ui.WINDOW_CLOSE, size="m"),
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
        ]
        childs.extend(base)
        super().__init__(
            vertical=True,
            hexpand=True,
            child=childs,
        )

        if popup and timeout > 0:
            _start_timeout(notification, self._scale, timeout)


class NotificationWidget(Box):
    def __init__(
        self,
        notification: Notification,
        popup: bool = False,
        timeout: int = notifications.popup_timeout,
    ) -> None:
        layout: NormalLayout | ScreenshotLayout

        if notification.app_name == "niri":
            layout = ScreenshotLayout(notification, popup, timeout)
        else:
            layout = NormalLayout(notification, popup, timeout)

        super().__init__(
            vertical=True,
            css_classes=["notification"],
            child=[layout],
            spacing=7,
        )
