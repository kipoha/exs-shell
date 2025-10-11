import asyncio

from dataclasses import dataclass

from ignis import widgets, utils
from ignis.window_manager import WindowManager

from base.window.animated import AnimatedWindowPopup

from config import config, user_config


window_manager = WindowManager.get_default()


@dataclass
class PowenMenuButton:
    name: str
    command: str
    icon: str | None = None


class PowerMenuItem(widgets.Button):
    def __init__(self, item: PowenMenuButton, **kwargs):
        super().__init__(**kwargs)
        self._action: PowenMenuButton = item

        super().__init__(
            on_click=lambda x: self.launch(),
            css_classes=["powermenu-action"],
            child=widgets.Box(
                child=[
                    widgets.Icon(image=self._action.icon, pixel_size=24),
                    widgets.Label(
                        label=self._action.name,
                        ellipsize="end",
                        max_width_chars=30,
                        css_classes=["powermenu-action-label"],
                    ),
                    self._menu,
                ],
                spacing=10,
            ),
        )

    def launch(self) -> None:
        asyncio.create_task(utils.exec_sh_async(self._action.command))
        window = window_manager.get_window(f"{config.NAMESPACE}_launcher")
        window.toggle()


actions = [PowenMenuButton(**action) for action in user_config.get("powermenu_actions", [])]


class PowenMenu(AnimatedWindowPopup):
    def __init__(
        self,
        **kwargs,
    ):
        self._main_box = widgets.Box(
            foo=...
        )
        super().__init__(
            namespace=f"{config.NAMESPACE}_powermenu",
            anchor=["bottom"],
            kb_mode = "on_demand",
            animation_duration=300,
            **kwargs,
        )
