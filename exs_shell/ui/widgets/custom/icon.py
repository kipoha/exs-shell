from typing import Any

from ignis.base_widget import BaseWidget
from ignis.widgets import Label

from exs_shell.interfaces.types import IconSize, IconType


class Icon(Label):
    """
    A widget that displays a Material icon.

    Inherits from :class:`ignis.widgets.label.Label`.

    This widget uses the ``Material Symbols`` font family.

    :param label:
        Name of the icon (see
        https://fonts.google.com/icons?icon.set=Material+Symbols).

    :param size:
        Icon size. One of: ``"xs"``, ``"s"``, ``"m"``, ``"l"``,
        ``"xl"``, ``"xxl"``, ``"xxxl"``.

    :param type:
        Icon style variant. One of: ``"Rounded"``,
        ``"Outlined"``, ``"Sharp"``.

    :param kwargs:
        Additional properties passed to :class:`ignis.Label`.

    Example
    -------

    .. code-block:: python

        Icon(
            label="close",
            size="l",
            type="Rounded",
        )
    """

    __gtype_name__ = "ExsIcon"
    __gproperties__ = {**BaseWidget.gproperties}

    def __init__(
        self,
        label: str,
        size: IconSize,
        type: IconType = "Rounded",
        **kwargs: Any,
    ):
        super().__init__(label=label, **kwargs)
        self._size: IconSize = size
        self._type: IconType = type

        self.add_css_class("icon")
        self._apply_classes()

    def _apply_classes(self):
        for cls in [
            "xs",
            "s",
            "m",
            "l",
            "xl",
            "xxl",
            "xxxl",
            "rounded",
            "sharp",
            "outlined",
        ]:
            self.remove_css_class(cls)

        self.add_css_class(self._size)
        self.add_css_class(self._type.lower())

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._apply_classes()

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
        self._apply_classes()
