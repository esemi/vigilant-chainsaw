"""Бот для фарминга игровых ресурсов."""

import logging
import time
from collections import Counter
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

import mss
from mss.models import Monitor

from bot.fishing.main import tick as fishing
from bot.state import State


@dataclass
class Resources(int, Enum):
    FISH = auto()


def select_monitor(sct) -> Monitor:
    return sct.monitors[-1]


def _farming_strategy(max_tick: Optional[int], state: State, counter: Counter, resource: Resources):
    with mss.mss() as sct:
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


def farm_bot(resource: Resources, debug_mode: bool = False, max_tick: Optional[int] = 5, start_delay: int = 5) -> Counter:
    counter = Counter()
    state = State(debug=debug_mode)
    logging.info('farm bot on %s %s %s', max_tick, start_delay, resource)
    time.sleep(start_delay)

    start_time = time.time()
    try:
        _farming_strategy(max_tick, state, counter, resource)
    except Exception as exc:
        logging.exception('exception captured', exc_info=exc)
    finally:
        fps = state.current_tick / (time.time() - start_time)
        logging.info('farm bot off %s; fps=%s', counter, fps)
    return counter


if __name__ == '__main__':
    # todo click parse cli options
    debug = True
    max_tick = 1

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    cnt = farm_bot(Resources.FISH, debug_mode=debug, max_tick=max_tick, start_delay=5)
    logging.info(cnt)
