from libexs import State
from loguru import logger


def init() -> None:
    if not State.services.niri.is_available:
        logger.error("Niri is not available")
        exit(1)
