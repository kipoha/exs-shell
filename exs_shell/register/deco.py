from typing import Callable, Any


def add_post_init(cls: type, hook: Callable[[Any], None]):
    original_init = cls.__init__

    if getattr(original_init, "_is_wrapped", False):
        cls._post_init_hooks.append(hook)  # type: ignore
        return

    cls._post_init_hooks = [hook]  # type: ignore

    def new_init(self, *args: Any, **kwargs: Any):
        original_init(self, *args, **kwargs)
        for h in cls._post_init_hooks:  # type: ignore
            h(self)

    setattr(new_init, "_is_wrapped", True)
    cls.__init__ = new_init  # type: ignore
