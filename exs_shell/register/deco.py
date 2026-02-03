from typing import Callable, Any

def add_post_init(cls: type, hook: Callable[[Any], None]):
    original_init = cls.__init__

    if getattr(original_init, "_is_wrapped", False):
        cls._post_init_hooks.append(hook)
        return

    cls._post_init_hooks = [hook]

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        for h in cls._post_init_hooks:
            h(self)

    setattr(new_init, "_is_wrapped", True)
    cls.__init__ = new_init
