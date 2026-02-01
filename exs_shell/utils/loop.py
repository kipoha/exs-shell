from typing import Any, TypeVar
from types import CoroutineType
from asyncio import create_task, get_event_loop, Task

T = TypeVar("T")


def run_async(func: CoroutineType[Any, Any, T]) -> T:
    loop = get_event_loop()
    return loop.run_until_complete(func)


def run_async_task(func: CoroutineType[Any, Any,T]) -> Task[T]:
    return create_task(func)
