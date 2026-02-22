from typing import Callable, TypeVar, Generic, Any, Type

R = TypeVar("R")

class classproperty(Generic[R]):
    def __init__(self, func: Callable[..., R]) -> None:
        self.func: Callable[[Type[Any]], R] = func

    def __get__(self, obj: Any, cls: Type[Any]) -> R:
        return self.func(cls)
