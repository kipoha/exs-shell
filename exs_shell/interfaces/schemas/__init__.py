from dataclasses import dataclass


@dataclass()
class IdleAction:
    timeout_seconds: int
    on_timeout: str
    on_resume: str | None
