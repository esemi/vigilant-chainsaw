import logging
import time
from collections import Counter
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

import mss as mss
from mss.models import Monitor

from bot import fishing
from bot.state import State


@dataclass
class Resources(int, Enum):
    FISH = auto()


def select_monitor(sct) -> Monitor:
    return sct.monitors[-1]


def farm_bot(
        resource: Resources,
        debug_mode: bool = False,
        limit_iterations: Optional[int] = 5,
        start_delay: int = 5,
) -> Counter:
    counter = Counter()
    state = State(debug=debug_mode)
    logging.info(f'farm bot on {limit_iterations=} {start_delay=} {resource=}')
    time.sleep(start_delay)

    with mss.mss() as sct:
        while state.current_tick < limit_iterations or limit_iterations is None:
            state.current_tick += 1
            counter['last_tick'] = state.current_tick

            monitor = select_monitor(sct)
            screenshot = sct.grab(monitor)

            if resource is Resources.FISH:
                next_action = fishing.tick(screenshot, state)
            else:
                raise NotImplementedError()
            logging.info(f'tick complete {next_action=}')

    logging.info(f'farm bot off {counter=}')
    return counter


if __name__ == '__main__':
    # todo click parse cli options
    # todo sigint handle
    debug = True

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    cnt = farm_bot(Resources.FISH, debug_mode=debug, limit_iterations=2, start_delay=5)
    logging.info(cnt)
