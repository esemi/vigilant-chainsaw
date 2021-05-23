from dataclasses import dataclass
from enum import auto, Enum


class Action(int, Enum):
    #  fishing: INIT -> WAITING_FOR_A_RUBBER -> WAITING_FOR_A_NIBBLE -> HOOKING_THE_FISH

    INIT = auto()
    WAITING_FOR_A_RUBBER = auto()
    WAITING_FOR_A_NIBBLE = auto()
    HOOKING_THE_FISH = auto()


@dataclass
class State:
    current_tick: int = 0
    action: Action = Action.INIT
    debug: bool = False

    def set_next_action(self, next_action: Action) -> Action:
        self.action = next_action
        return next_action

    def skip_to_init(self) -> Action:
        self.action = Action.INIT
        return self.action
