from ignis.widgets import Label
from exs_shell import register


@register.event
class CavaLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(label="", css_classes=["cava"], **kwargs)

    @register.events.cava("text")
    def _update_label(self, visual: str):
        self.label = visual
