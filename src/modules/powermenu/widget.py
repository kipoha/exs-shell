import asyncio

from dataclasses import dataclass

from ignis import widgets, utils
from ignis.window_manager import WindowManager

from base.window.animated import AnimatedWindowPopup

from config import config
from config.user import options
from base.singleton import SingletonClass


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




class PowenMenu(AnimatedWindowPopup, SingletonClass):
    def __init__(
        self,
        **kwargs,
    ):
        self.actions = [PowenMenuButton(**action) for action in options.user_config.powermenu_actions]
        self.buttons = widgets.Box(
            css_classes=["powermenu-actions"],
            vertical=True,
            child=[PowerMenuItem(item=item) for item in self.actions],
            spacing=10,
        )
        self._main_box = widgets.Box(
            css_classes=["powermenu"], child=[self.buttons] 
        )
        super().__init__(
            namespace=f"{config.NAMESPACE}_powermenu",
            anchor=["right"],
            kb_mode = "on_demand",
            animation_duration=300,
            visible=True,
            layer="overlay",
            child=self._main_box,
            **kwargs,
        )

        options.user_config.connect_option("powermenu_actions", self.update_actions)

    def update_actions(self):
        self.actions = [PowenMenuButton(**action) for action in options.user_config.powermenu_actions]
