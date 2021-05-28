"""Методы работы с состоянием контекста для обработчиков игровых тиков."""

from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Optional

from bot.gui import Area, Point


class Action(IntEnum):
    INIT = auto()
    START = auto()
    WAITING_FOR_A_BOBBER = auto()
    WAITING_FOR_A_NIBBLE = auto()
    WAITING_FOR_A_HOOKING_GAME = auto()
    HOOKING_THE_FISH = auto()


@dataclass
class MetaInfo(object):
    target_point: Optional[Point] = None
    bobber_area: Optional[Area] = None
    game_area: Optional[Area] = None
    nibble_tick_counter: int = 0


@dataclass
class State(object):
    current_tick: int = 0
    action: Action = Action.INIT
    debug: bool = False
    meta: MetaInfo = MetaInfo()

    def __post_init__(self):
        self._meta = {}

    def set_next_action(self, next_action: Action) -> Action:
        self.action = next_action  # noqa: WPS601
        return self.action
