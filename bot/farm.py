"""Бот для фарминга игровых ресурсов."""

import logging
import time
from collections import Counter
from typing import Callable, Optional

from mss import models, mss  # type: ignore

from bot.fishing import main as fishing
from bot.harvesting import main as harvesting
from bot.resources import Resources
from bot.state import Action, State


def select_monitor(sct) -> models.Monitor:
    return sct.monitors[-1]


def _farming_strategy(farm_method: Callable, max_tick: Optional[int], state: State, counter: Counter, auto_restart: bool):
    with mss() as sct:
        while max_tick is None or state.current_tick < max_tick:
            state.current_tick += 1
            counter['last_tick'] = state.current_tick

            monitor = select_monitor(sct)
            frame = sct.grab(monitor)

            logging.info('tick %s', state.current_tick)
            try:
                next_action = farm_method(frame, state)

            except AssertionError as exc:
                if auto_restart:
                    logging.error('Restart after error', exc_info=exc)
                    state.set_next_action(Action.START)
                else:
                    raise exc
            logging.info('tick complete %s', next_action)


def select_farming_module(resource: Resources) -> Callable:
    if resource is Resources.FISH:
        return fishing.tick

    if resource is Resources.COTTON:
        return harvesting.tick

    raise NotImplementedError()


def farm_bot(
    resource: Resources,
    debug_mode: bool = False,
    tick_limit: Optional[int] = 5,
    start_delay: int = 5,
    restart_if_error: bool = False,
) -> Counter:
    counter: Counter = Counter()
    state = State(debug=debug_mode)
    logging.info('farm bot on %s %s %s', tick_limit, start_delay, resource)
    time.sleep(start_delay)

    start_time = time.time()

    farm_method = select_farming_module(resource)

    try:
        _farming_strategy(farm_method, tick_limit, state, counter, restart_if_error)
    except Exception as exc:
        logging.exception('exception captured', exc_info=exc)
    finally:
        fps = state.current_tick / (time.time() - start_time)
        logging.info('farm bot off %s; fps=%s', counter, fps)
    return counter


if __name__ == '__main__':
    debug = True
    tick_limit = None
    ignore_fail = True

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    cnt = farm_bot(
        Resources.COTTON,
        debug_mode=debug,
        tick_limit=tick_limit,
        start_delay=5,
        restart_if_error=ignore_fail,
    )
    logging.info(cnt)
