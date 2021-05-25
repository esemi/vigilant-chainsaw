"""Реализация всех возможных стратегий алгоритма фарма конкретного ресурса."""

import logging
import random
import time

from numpy import ndarray

from bot import settings
from bot.fishing import cv_helpers
from bot.gui import Area, Point, left_click, mouse_move_to
from bot.state import State


def init_action(state: State, gray_frame: ndarray) -> Point:
    # ищем персонажа
    character_coords = cv_helpers.search_character(state, gray_frame)
    logging.debug('found character coords %s', character_coords)
    assert character_coords, 'Character not found'
    character_point = character_coords[0]

    # ищем воду
    water_coords = cv_helpers.search_water_cell(state, gray_frame)
    logging.debug('found water cell coords %s', len(water_coords))
    assert water_coords, 'Water cells not found'

    # select nearest water cell
    fishing_cell = cv_helpers.choice_cell_for_fishing(state, gray_frame, character_point, water_coords)
    logging.debug('select cell for click %s', fishing_cell)
    return fishing_cell


def start_fishing_action(state: State, gray_frame: ndarray, target: Point):
    # левый клик
    mouse_move_to(target)
    left_click(settings.FISHING_CLICK_DURATION)
    mouse_move_to(Point(
        x=target.x + random.randint(110, 150),  # noqa: WPS432
        y=target.y - random.randint(2, 11),  # noqa: WPS432
    ))

    # Поплавок может появиться не сразу после заброса удочки, потому ждём какое то время для поиска.
    time.sleep(settings.FISHING_BOBBER_SEARCH_DELAY)

    cv_helpers.show_current_frame(state, gray_frame, 'fishing action')


def wait_for_bobber_action(state: State, gray_frame: ndarray) -> Area:
    # ищем персонажа
    character_coords = cv_helpers.search_character(state, gray_frame)
    logging.debug('found character coords %s', character_coords)
    assert character_coords, 'Character not found'
    character_point = character_coords[0]

    # ищем поплавок
    bobber_areas = cv_helpers.search_bobber(state, gray_frame, character_point)
    logging.debug('found bobbers %s', bobber_areas)
    assert bobber_areas, 'Not found bobber'
    return bobber_areas[0]


def wait_for_nibble_action(state: State, gray_frame: ndarray, bobber_area: Area) -> bool:
    # ищем поплавок в подводном положении в заданой области экрана
    need_hooking_the_fish = cv_helpers.looking_for_nibbles(state, gray_frame, bobber_area)
    logging.debug('need_hooking_the_fish=%s', need_hooking_the_fish)
    if need_hooking_the_fish:
        mouse_move_to(bobber_area.from_point, float(0))
        left_click(settings.FISHING_CLICK_DURATION)

    return need_hooking_the_fish


def hooking_the_fish_action(state: State, gray_frame: ndarray) -> bool:
    # todo ищем поплавок-ползунок
    # todo кликаем если отклонился от середины влево
    # todo некликаем если отклонился от середины вправо
    # todo ждём пока он пропадёт
    raise NotImplementedError()
