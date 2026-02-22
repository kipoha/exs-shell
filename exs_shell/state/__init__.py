from typing import Any


class AttrDict(dict):
    def __getattr__(self, key: str) -> Any:
        if key in self:
            value = self[key]
            if isinstance(value, dict) and not isinstance(value, AttrDict):
                value = AttrDict(value)
                self[key] = value
            return value

        if hasattr(dict, key):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

        value = AttrDict()
        self[key] = value
        return value

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value


class _State(AttrDict):
    pass


State = _State()
