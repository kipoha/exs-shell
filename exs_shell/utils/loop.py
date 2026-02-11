from threading import Thread
from typing import Any, Callable, Coroutine
from asyncio import create_task, get_event_loop, Task


def run_async[T](func: Coroutine[Any, Any, T]) -> T:
    loop = get_event_loop()
    return loop.run_until_complete(func)


def run_async_task[T](func: Coroutine[Any, Any, T]) -> Task[T]:
    return create_task(func)


def thread(target: Callable, *args, **kwargs) -> Thread:
    thread = Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread


def run_in_thread(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        return thread(func, *args, **kwargs)

    return wrapper
