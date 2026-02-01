from ignis import widgets

from exs_shell_deprecated.base.singleton import SingletonClass
from exs_shell_deprecated.config.user import options
from exs_shell_deprecated.modules.dashboard.widgets.cava import AudioVisualizer
from exs_shell_deprecated.modules.bar.childs.battery.widget import Battery
from exs_shell_deprecated.modules.bar.childs.clock.widget import Clock
from exs_shell_deprecated.modules.bar.childs.layout.widget import KeyboardLayout


class LockScreenTopBar(widgets.CenterBox, SingletonClass):
    def __init__(self, **kwargs):
        self.__avatar = widgets.Picture(
            content_fit="cover",
            width=50,
            height=50,
            image=options.user_config.bind("avatar"),
            css_classes=["lockscreen-top-bar-avatar-image"],
        )
        self.__avatar_box = widgets.Box(
            css_classes=["lockscreen-top-bar-avatar"],
            child=[self.__avatar],
        )
        self.cava_left = AudioVisualizer(height=10, css_classes=["lockscreen-audio-visualizer-left"])
        self.cava_right = AudioVisualizer(height=10, mirror=True, css_classes=["lockscreen-audio-visualizer-right"])
        self.__battery = Battery()
        self.__battery_box = widgets.Box(
            css_classes=["lockscreen-top-bar-battery"],
            child=[self.__battery],
        )
        self.__clock = Clock()
        self.__clock_box = widgets.Box(
            css_classes=["lockscreen-top-bar-clock"],
            child=[self.__clock],
        )

        self.__keyboard_layout_box = KeyboardLayout(
            css_classes=["lockscreen-top-bar-keyboard-layout"],
        )

        self.left_center_corner = widgets.Corner(
            orientation="top-right",
            width_request=50,
            height_request=40,
            css_classes=["lockscreen-top-bar-left-center-corner"],
            halign="end",
            valign="start",
        )

        self.right_center_corner = widgets.Corner(
            orientation="top-left",
            width_request=50,
            height_request=40,
            css_classes=["lockscreen-top-bar-right-center-corner"],
            halign="end",
            valign="start",
        )

        self.left_right_corner = widgets.Corner(
            orientation="top-right",
            width_request=50,
            height_request=50,
            css_classes=["lockscreen-top-bar-left-right-corner"],
            halign="end",
            valign="start",
        )

        self.right_left_corner = widgets.Corner(
            orientation="top-left",
            width_request=50,
            height_request=50,
            css_classes=["lockscreen-top-bar-right-left-corner"],
            halign="end",
            valign="start",
        )

        self.center_box = widgets.Box(
            css_classes=["lockscreen-top-bar-center"],
            child=[self.cava_left, self.__avatar_box, self.cava_right],
            spacing=10,
            valign="center",
            halign="center",
        )

        self.right_box = widgets.Box(
            spacing=20,
            css_classes=["lockscreen-top-bar-right"],
            child=[self.__clock_box, self.__battery_box],
        )

        self.left_box = widgets.Box(
            css_classes=["lockscreen-top-bar-left"],
            child=[self.__keyboard_layout_box],
        )


        self.center_container = widgets.Box(
            child=[self.left_center_corner, self.center_box, self.right_center_corner],
        )

        self.right_container = widgets.Box(
            child=[self.left_right_corner, self.right_box],
        )

        self.left_container = widgets.Box(
            child=[self.left_box, self.right_left_corner],
        )


        super().__init__(
            css_classes=["lockscreen-top-bar-container"],
            start_widget=self.left_container,
            center_widget=self.center_container,
            end_widget=self.right_container,
            **kwargs,
        )
