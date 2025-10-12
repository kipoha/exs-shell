from ignis import widgets
from ignis.services.niri import NiriService


class KeyboardLayout(widgets.EventBox):
    def __init__(self, **kwargs):
        niri_service = NiriService.get_default()
        super().__init__(
            on_click=lambda x: niri_service.switch_kb_layout(),
            child=[widgets.Label(label=niri_service.keyboard_layouts.bind("current_name"))],
            **kwargs
        )
