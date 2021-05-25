import logging  # noqa
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

    start_time = time.time()
    try:
        with mss.mss() as sct:
            while limit_iterations is None or state.current_tick < limit_iterations:
                state.current_tick += 1
                counter['last_tick'] = state.current_tick

                monitor = select_monitor(sct)
                screenshot = sct.grab(monitor)

                if resource is Resources.FISH:
                    logging.info('tick %d', state.current_tick)
                    next_action = fishing.tick(screenshot, state)
                    logging.info('tick complete %s', next_action)
                else:
                    raise NotImplementedError()
    except Exception as exc:
        logging.exception('exception captured', exc_info=exc)
    finally:
        fps = state.current_tick / (time.time() - start_time)
        logging.info(f'farm bot off {counter=} {fps=}')
    return counter


if __name__ == '__main__':
    # todo click parse cli options
    # todo sigint handle
    debug = False

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    cnt = farm_bot(Resources.FISH, debug_mode=debug, limit_iterations=500, start_delay=5)
    logging.info(cnt)
