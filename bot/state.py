import logging
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any


class Action(int, Enum):
    #  fishing: INIT -> WAITING_FOR_A_RUBBER -> WAITING_FOR_A_NIBBLE -> HOOKING_THE_FISH

    INIT = auto()
    WAITING_FOR_A_BOBBER = auto()
    WAITING_FOR_A_NIBBLE = auto()
    HOOKING_THE_FISH = auto()


@dataclass
class State:
    current_tick: int = 0
    action: Action = Action.INIT
    debug: bool = False

    def __post_init__(self):
        self._meta = {}
        self.reset()

    def set_next_action(self, next_action: Action) -> Action:
        self.action = next_action
        return self.action

    def reset(self) -> Action:
        self._meta = {}  # noqa
        self.action = Action.INIT
        return self.action

    def put_meta(self, key_: str, value: Any):
        self._meta[key_] = value
        logging.debug(f'put meta {key_} = {value=}')

    def fetch_meta(self, key_: str, default: Any = None) -> Any:
        value = self._meta.get(key_, default)
        logging.debug(f'pop meta {key_} = {value=}')
        return value
