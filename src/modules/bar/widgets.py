from ignis import widgets

from base.singleton import SingletonClass

from config.user import options


class BarWidgets(SingletonClass):
    def __init__(self) -> None:
        from modules.bar.childs import modules

        self.modules = modules

        self._left = widgets.Box(
            child=[modules[module]() for module in options.bar.left],
            spacing=options.bar.left_spacing,
        )

        self._center = widgets.Box(
            child=[modules[module]() for module in options.bar.center],
            spacing=options.bar.center_spacing,
        )

        self._right = widgets.Box(
            child=[modules[module]() for module in options.bar.right],
            spacing=options.bar.right_spacing,
        )

        # options.bar.connect_option("left", self.update_left)
        # options.bar.connect_option("center", self.update_center)
        # options.bar.connect_option("right", self.update_right)

    @property
    def left(self) -> widgets.Box:
        return self._left

    @property
    def center(self) -> widgets.Box:
        return self._center

    @property
    def right(self) -> widgets.Box:
        return self._right

bar_widgets = BarWidgets.get_default()

left = bar_widgets.left
center = bar_widgets.center
right = bar_widgets.right
# def left(monitor_name) -> widgets.Box:
#     from modules.bar.childs import modules
#
#     return widgets.Box(child=[modules["tray"]()], spacing=10)
#
#
# def center(monitor_name) -> widgets.Box:
#     from modules.bar.childs import modules
#
#     return widgets.Box(
#         child=[
#             modules["clock"](),
#             modules["cava"](),
#         ],
#         spacing=20,
#     )
#
#
# def right(monitor_name) -> widgets.Box:
#     from modules.bar.childs import modules
#
#     return widgets.Box(
#         child=[
#             modules["layout"](),
#             modules["battery"](),
#         ],
#         spacing=10,
#     )
