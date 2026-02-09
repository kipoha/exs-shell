from typing import Any

from ignis import utils
from ignis.services.notifications import Notification, NotificationService
from ignis.widgets import Box

from exs_shell import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.gtk.windows import Layer
from exs_shell.state import State
from exs_shell.ui.factory import window
from exs_shell.ui.modules.notification.shared import NotificationWidget
from exs_shell.ui.widgets.base import RevealerBaseWidget
from exs_shell.ui.widgets.windows import Revealer


@register.event
class Popup(Box):
    def __init__(
        self, box: "PopupBox", window: "NotificationPopup", notification: Notification
    ):
        self._box = box
        self._window = window
        self.notification = notification
        self.notifications: NotificationService = State.services.notifications

        widget = NotificationWidget(notification)
        widget.css_classes = ["notification-popup"]

        self._inner = Revealer(transition_type=RevealerTransition.SLIDE_UP, child=widget, transition_duration=250)
        self._outer = Revealer(transition_type=RevealerTransition.SLIDE_DOWN, child=self._inner, transition_duration=250)
        super().__init__(child=[self._outer], halign="end")

    @register.events.notifications("dismissed", True)
    def destroy(self, *_: Any):
        def box_destroy():
            self.unparent()
            if len(self.notifications.popups) == 0:
                self._window.visible = False

        def outer_close():
            self._outer.reveal_child = False
            utils.Timeout(self._outer.transition_duration, box_destroy)

        self._inner.transition_type = RevealerTransition.SLIDE_DOWN
        self._inner.reveal_child = False
        utils.Timeout(self._outer.transition_duration, outer_close)


@register.event
class PopupBox(Box):
    def __init__(self, window: "NotificationPopup"):
        self._window = window

        super().__init__(
            vertical=True,
            valign="start",
        )

    @register.events.notifications("new_popup")
    def __on_notified(self, _: Any, notification: Notification) -> None:
        self._window.visible = True
        popup = Popup(box=self, window=self._window, notification=notification)
        self.prepend(popup)
        popup._outer.reveal_child = True
        utils.Timeout(
            popup._outer.transition_duration, popup._inner.set_reveal_child, True
        )


class NotificationPopup(RevealerBaseWidget):
    def __init__(
        self,
        monitor_id: int,
        transition_type: RevealerTransition = RevealerTransition.NONE,
        transition_duration: int = 0,
        reveal_child: bool = False,
    ) -> None:
        win = window.create(
            anchor=["right", "top", "bottom"],
            namespace=f"notification_popup{monitor_id}",
            monitor=monitor_id,
            layer=Layer.TOP,
            visible=False,
            dynamic_input_region=True,
            css_classes=["notification-popup-window"],
            style="min-width: 29rem;",
        )
        self._box = PopupBox(window=self)
        super().__init__(
            self._box, win, transition_type, transition_duration, reveal_child
        )
