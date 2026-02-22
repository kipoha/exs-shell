from typing import Any, Sequence

from ignis.base_widget import BaseWidget
from ignis.widgets import Box


class BaseTab(Box):
    def __init__(self, child: Sequence[BaseWidget] | None = None, **kwargs: Any):
        super().__init__(
            vertical=True,
            spacing=8,
            css_classes=["settings-body"],
            hexpand=False,
            halign="center",
            width_request=900,
            child=child,
            **kwargs,
        )


class BaseCategory(Box):
    def __init__(self, child: Sequence[BaseWidget] | None = None, **kwargs: Any):
        super().__init__(
            child=child,
            css_classes=["settings-category"],
            vertical=True,
            spacing=0,
            **kwargs,
        )
