"""Бот для фарминга игровых ресурсов."""

import logging
import time
from collections import Counter
from typing import Callable, Optional

import click
from mss import models, mss  # type: ignore

from bot.fishing import main as fishing
from bot.harvesting import main as harvesting
from bot.resources import Resources
from bot.state import Action, State


def select_monitor(sct) -> models.Monitor:
    return sct.monitors[-1]


def _farming_strategy(
    farm_method: Callable,
    max_tick: Optional[int],
    state: State,
    counter: Counter,
    auto_restart: bool,
):
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


def farm_bot(resource: Resources, debug_mode: bool, tick_limit: Optional[int], start_delay: int = 5) -> Counter:
    counter: Counter = Counter()
    state = State(debug=debug_mode)
    logging.info('farm bot on %s %s %s', tick_limit, start_delay, resource)
    time.sleep(start_delay)

    start_time = time.time()

    farm_method = select_farming_module(resource)

    try:
        _farming_strategy(farm_method, tick_limit, state, counter, auto_restart=True)
    except Exception as exc:
        logging.exception('exception captured', exc_info=exc)
    finally:
        fps = state.current_tick / (time.time() - start_time)
        logging.info('farm bot off %s; fps=%s', counter, fps)
    return counter


@click.command()
@click.option(
    '--resource',
    required=True,
    type=click.Choice(['fish', 'cotton']),
    help='Farming resource name',
)
@click.option('--limit', required=True, type=int, help='Farming tick limit')
@click.option('--verbose', type=bool, default=False, help='Enables verbose mode')
def runner(resource: str, limit: int, verbose: bool = False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
    farm_bot(Resources(resource), verbose, limit)
