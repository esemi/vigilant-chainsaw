import copy
import logging
import operator
import random
import time
from pathlib import Path
from typing import List, Union

import cv2
import numpy
import numpy as np
from PIL import Image
from mss.screenshot import ScreenShot
from numpy import ndarray

from bot import settings
from bot.cv_operations import mark_coords, templates_client, mark_template
from bot.gui import Point, mouse_move_to, left_click, Area
from bot.state import State, Action

DEBUG_FRAMES_COUNTER = 0


def tick(screenshot: ScreenShot, state: State) -> Action:
    """Фармим рыбалку.

    - ищем ближайшую клетку с водой и забрасываем удочку
    - ждём пока поплавок скроется под водой и дёргаем
    - подсекаем рыбу пока миниагра с ползунком не исчезнет
    - повторяем

    INIT -> WAITING_FOR_A_RUBBER -> WAITING_FOR_A_NIBBLE -> HOOKING_THE_FISH ->> INIT -> ...

    """
    logging.debug('tick %d %s', state.current_tick, state)

    show_current_frame(state, screenshot, 'init screen')

    color_frame = numpy.array(screenshot)
    gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
    show_current_frame(state, gray_frame, 'init screen gray')

    character_coords = _search_character(state, gray_frame)
    logging.info(f'found character coords {character_coords}')
    assert character_coords, 'Character not found'
    character_point = character_coords[0]

    if state.action == Action.INIT:
        # забрасываем удочку
        _init_action(state, gray_frame, character_point)
        return state.set_next_action(Action.WAITING_FOR_A_RUBBER)

    elif state.action == Action.WAITING_FOR_A_RUBBER:
        # ждём пока появится поплавок над водой
        rubber_area = _wait_for_rubber_action(state, gray_frame, character_point)
        return state.set_next_action(Action.WAITING_FOR_A_NIBBLE)

    elif state.action == Action.WAITING_FOR_A_NIBBLE:
        # ждём клёва
        return state.set_next_action(Action.HOOKING_THE_FISH)

    elif state.action == Action.HOOKING_THE_FISH:
        # подсекаем рыбу

        # todo ищем поплавок-ползунок
        # todo кликаем если отклонился от середины влево
        # todo некликаем если отклонился от середины вправо
        # todo ждём пока он пропадёт

        return state.skip_to_init()


def locations_to_points(locations: ndarray) -> List[Point]:
    return [Point(x=from_x, y=from_y) for from_x, from_y in zip(*locations[::-1])]


def show_current_frame(state: State, frame: Union[ScreenShot, ndarray], message: str):
    global DEBUG_FRAMES_COUNTER
    if not state.debug:
        return

    DEBUG_FRAMES_COUNTER += 1

    debug_folder = Path('../data/debug/')
    filepath = str(debug_folder / f'frame#{DEBUG_FRAMES_COUNTER}-tick#{state.current_tick}-{message}.png')
    if type(frame) is ScreenShot:
        img = Image.frombytes('RGB', frame.size, frame.bgra, 'raw', 'BGRX')
        img.thumbnail((1024, 512))
        img.save(filepath)
    else:
        cv2.imwrite(filepath, frame)

    logging.debug(message)


def _init_action(state: State, gray_frame: ndarray, character_point: Point):
    # ищем воду
    water_coords = _search_water_cell(state, gray_frame)
    logging.info(f'found water cell coords {len(water_coords)}')
    logging.debug(f'{water_coords}')
    assert water_coords, 'Water cells not found'

    # todo feature: clustering all cells and select center of greatest cluster for determine fishing direction

    # select nearest water cell
    available_water_cells = list(filter(
        lambda p: p.distance(character_point) <= settings.FISHING_DISTANCE,
        water_coords,
    ))
    assert available_water_cells, 'Not found available water cells for fishing'
    logging.info(f'filtering available cell for fishing {len(available_water_cells)}')
    logging.debug(f'{available_water_cells}')
    for point in available_water_cells:
        mark_coords(gray_frame, point)
    show_current_frame(state, gray_frame, 'available water cells')

    fishing_cell = random.choice(available_water_cells)
    logging.info(f'select cell for click {fishing_cell}')

    # левый клик
    mouse_move_to(fishing_cell)
    left_click(settings.FISHING_CLICK_DURATION)

    # Поплавок может появиться не сразу после заброса удочки, потому ждём какое то время для поиска.
    time.sleep(settings.FISHING_BOBBER_SEARCH_DELAY)

    show_current_frame(state, gray_frame, 'waiting for a nibble')


def _wait_for_rubber_action(state: State, gray_frame: ndarray, character_point: Point):
    # todo ищем поплавок
    _search_bobber(state, gray_frame, character_point)
    # todo ждём пока он пропадёт
    # todo левый клик
    pass


def _search_water_cell(state: State, gray_frame: ndarray) -> List[Point]:
    show_current_frame(state, gray_frame, 'search water cell')

    tpl = templates_client.water_template
    tpl_width, tpl_height = tpl.shape[::-1]

    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.7)

    center_points = list(map(
        lambda p: Point(x=p.x + int(tpl_width / 2), y=p.y + int(tpl_height / 2)),
        locations_to_points(loc),
    ))

    tmp_frame = copy.copy(gray_frame)
    for point in center_points:
        mark_coords(tmp_frame, point)
    show_current_frame(state, tmp_frame, 'search water cells')
    return center_points


def _search_character(state: State, gray_frame: ndarray) -> List[Point]:
    """Ищем координаты персонажа."""
    show_current_frame(state, gray_frame, 'search character')

    tpl = templates_client.character_template
    tpl_width, tpl_height = tpl.shape[::-1]

    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.8)
    source_points = locations_to_points(loc)

    for from_point in source_points:
        to_point = Point(x=from_point.x + tpl_width, y=from_point.y + tpl_height)
        mark_template(gray_frame, from_point, to_point)
    show_current_frame(state, gray_frame, 'search character match')

    center_points = list(map(
        lambda p: Point(x=p.x + int(tpl_width / 2), y=p.y + int(tpl_height / 2)),
        source_points,
    ))
    for point in center_points:
        mark_coords(gray_frame, point)
    show_current_frame(state, gray_frame, 'search character coords')

    return center_points


def _search_bobber(state: State, gray_frame: ndarray, character_point: Point) -> List[Point]:
    """Ищем поплавок на воде."""

    show_current_frame(state, gray_frame, 'search bobber')

    tpl = templates_client.bobber_template
    tpl_width, tpl_height = tpl.shape[::-1]

    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.7)
    source_points = locations_to_points(loc)

    tmp_frame = copy.deepcopy(gray_frame)
    for from_point in source_points:
        to_point = Point(x=from_point.x + tpl_width, y=from_point.y + tpl_height)
        mark_template(tmp_frame, from_point, to_point)

    show_current_frame(state, tmp_frame, 'search bobber cells')

    # выбираем ближайший к нам поплавок
    points_by_distance = sorted([(point, point.distance(character_point)) for point in source_points], key=operator.itemgetter(1))
    logging.debug(f'rubbers by distance from character {points_by_distance=}')
    show_current_frame(state, tmp_frame, 'filter nearest bobber')

    return list(map(operator.itemgetter(0), points_by_distance))
