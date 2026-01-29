from typing import Any


class _State:
    def __init__(self) -> None:
        self.__dict__["_store"] = {}

    def __getattr__(self, item: str) -> Any:
        return self._store.get(item, None)

    def __setattr__(self, key: str, value: Any) -> None:
        self._store[key] = value


State = _State()
