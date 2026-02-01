from typing import Any


class AttrDict(dict):
    def __getattr__(self, key: str) -> Any:
        if key not in self:
            value = AttrDict()
            self[key] = value
            return value

        value = self[key]
        if isinstance(value, dict) and not isinstance(value, AttrDict):
            value = AttrDict(value)
            self[key] = value

        return value

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value


class _State(AttrDict):
    pass


State = _State()
