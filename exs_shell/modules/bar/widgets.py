from ignis import widgets

from exs_shell.base.singleton import SingletonClass

from exs_shell.config.user import options


class BarWidgets(SingletonClass):
    def __init__(self) -> None:
        from exs_shell.modules.bar.childs import modules

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

        options.bar.connect_option("left", self.update_left)
        options.bar.connect_option("center", self.update_center)
        options.bar.connect_option("right", self.update_right)
        options.bar.connect_option("left_spacing", self.update_left_spacing)
        options.bar.connect_option("center_spacing", self.update_center_spacing)
        options.bar.connect_option("right_spacing", self.update_right_spacing)

    def update_left(self, *_):
        self._update_box(self._left, options.bar.left)

    def update_center(self, *_):
        self._update_box(self._center, options.bar.center)

    def update_right(self, *_):
        self._update_box(self._right, options.bar.right)

    def update_left_spacing(self, *_):
        self._left.spacing = options.bar.left_spacing

    def update_center_spacing(self, *_):
        self._center.spacing = options.bar.center_spacing

    def update_right_spacing(self, *_):
        self._right.spacing = options.bar.right_spacing

    def _update_box(self, box: widgets.Box, module_names: list[str]):
        for child in list(box.child):  # type: ignore
            box.remove(child)

        for name in module_names:
            if name in self.modules:
                box.append(self.modules[name]())

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
