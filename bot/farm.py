"""Бот для фарминга игровых ресурсов."""

import logging
import time
from collections import Counter
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

from mss import models, mss  # type: ignore

from bot.fishing.main import tick as fishing
from bot.state import State


@dataclass
class Resources(int, Enum):
    FISH = auto()


def select_monitor(sct) -> models.Monitor:
    return sct.monitors[-1]


def _farming_strategy(max_tick: Optional[int], state: State, counter: Counter, resource: Resources):
    with mss() as sct:
        while max_tick is None or state.current_tick < max_tick:
            state.current_tick += 1
            counter['last_tick'] = state.current_tick

            monitor = select_monitor(sct)
            screenshot = sct.grab(monitor)

            if resource is Resources.FISH:
                logging.info('tick %s', state.current_tick)
                next_action = fishing(screenshot, state)
                logging.info('tick complete %s', next_action)
            else:
                raise NotImplementedError()


def farm_bot(resource: Resources, debug_mode: bool = False, tick_limit: Optional[int] = 5, start_delay: int = 5) -> Counter:
    counter: Counter = Counter()
    state = State(debug=debug_mode)
    logging.info('farm bot on %s %s %s', tick_limit, start_delay, resource)
    time.sleep(start_delay)

    start_time = time.time()
    try:
        _farming_strategy(tick_limit, state, counter, resource)
    except Exception as exc:
        logging.exception('exception captured', exc_info=exc)
    finally:
        fps = state.current_tick / (time.time() - start_time)
        logging.info('farm bot off %s; fps=%s', counter, fps)
    return counter


if __name__ == '__main__':
    # todo click parse cli options
    debug = True
    tick_limit = 1

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    cnt = farm_bot(Resources.FISH, debug_mode=debug, tick_limit=tick_limit, start_delay=5)
    logging.info(cnt)
