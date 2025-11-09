import asyncio

from dataclasses import dataclass

from ignis import widgets, utils
from ignis.window_manager import WindowManager

from exs_shell.base.window.animated import PartiallyAnimatedWindow
from exs_shell.base.singleton import SingletonClass
from exs_shell.config import config
from exs_shell.config.user import options


window_manager = WindowManager.get_default()


@dataclass
class PowenMenuButton:
    command: str
    icon: str


class PowerMenuItem(widgets.Button):
    def __init__(self, item: PowenMenuButton, **kwargs):
        self._action: PowenMenuButton = item

        super().__init__(
            on_click=lambda x: self.launch(),
            css_classes=["powermenu-action"],
            child=widgets.Box(
                child=[
                    widgets.Label(
                        label=self._action.icon,
                        ellipsize="end",
                        max_width_chars=30,
                        css_classes=["powermenu-action-label"],
                    ),
                ],
                spacing=10,
            ),
        )

    def launch(self) -> None:
        asyncio.create_task(utils.exec_sh_async(self._action.command))
        window = window_manager.get_window(f"{config.NAMESPACE}_powermenu")
        window.toggle()


class PowenMenu(PartiallyAnimatedWindow, SingletonClass):
    def __init__(
        self,
        **kwargs,
    ):
        self.actions = [
            PowenMenuButton(**action)
            for action in options.user_config.powermenu_actions
        ]
        self.buttons = widgets.Box(
            css_classes=["powermenu-actions"],
            vertical=True,
            child=[PowerMenuItem(item=item) for item in self.actions],
            spacing=10,
        )
        self._box = widgets.Box(css_classes=["powermenu-box"], child=[self.buttons])
        self.top_corner = widgets.Corner(
            css_classes=["powermenu-top-corner"],
            orientation="bottom-right",
            height_request=50,
            width_request=70,
            halign="end",
            valign="end",
        )
        self.bottom_corner = widgets.Corner(
            css_classes=["powermenu-bottom-corner"],
            orientation="top-right",
            height_request=50,
            width_request=70,
            halign="end",
            valign="end",
        )
        self._main_box = widgets.EventBox(
            css_classes=["powermenu"],
            vertical=True,
            child=[self.top_corner, self._box, self.bottom_corner],
            on_hover_lost=self._on_mouse_leave,
        )

        self._animated_parts = [self.top_corner, self.bottom_corner, self._box]

        super().__init__(
            namespace=f"{config.NAMESPACE}_powermenu",
            anchor=["right"],
            kb_mode="on_demand",
            animation_duration=300,
            visible=True,
            layer="overlay",
            child=self._main_box,
            **kwargs,
        )

        options.user_config.connect_option("powermenu_actions", self.update_actions)

    def update_actions(self):
        self.actions = [
            PowenMenuButton(**action)
            for action in options.user_config.powermenu_actions
        ]
    
    def _on_mouse_leave(self, *_):
        self.close()


class PowerMenuTrigger(PartiallyAnimatedWindow, SingletonClass):
    SENSOR_HEIGHT = 400
    SENSOR_WIDTH = 4

    def __init__(self):
        self.powermenu = PowenMenu.get_default()

        trigger_box = widgets.EventBox(
            vexpand=False,
            hexpand=True,
            height_request=self.SENSOR_HEIGHT,
            width_request=self.SENSOR_WIDTH,
            on_hover=self._on_hover,
            css_classes=["powermenu-trigger"],
        )

        super().__init__(
            namespace=f"{config.NAMESPACE}_powermenu_trigger",
            anchor=["right"],
            visible=True,
            child=trigger_box,
        )

    def _on_hover(self, *_):
        self.powermenu.open()
