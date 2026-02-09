from typing import Any, Coroutine
from asyncio import create_task, get_event_loop, Task


def run_async[T](func: Coroutine[Any, Any, T]) -> T:
    loop = get_event_loop()
    return loop.run_until_complete(func)


def run_async_task[T](func: Coroutine[Any, Any, T]) -> Task[T]:
    return create_task(func)
