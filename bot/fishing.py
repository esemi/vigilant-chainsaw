import copy
import logging
import random
import time
from typing import List, Union

import cv2
import numpy
import numpy as np
from PIL import Image
from mss.screenshot import ScreenShot
from numpy import ndarray

from bot import settings
from bot.cv_operations import mark_point, templates_client, mark_area
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
    logging.info('tick %d %s', state.current_tick, state)

    show_current_frame(state, screenshot, 'init screen')

    color_frame = numpy.array(screenshot)
    gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
    show_current_frame(state, gray_frame, 'init screen gray')

    if state.action == Action.INIT:
        # забрасываем удочку
        _init_action(state, gray_frame)
        return state.set_next_action(Action.WAITING_FOR_A_BOBBER)

    elif state.action == Action.WAITING_FOR_A_BOBBER:
        # ждём пока появится поплавок над водой
        bobber_area = _wait_for_bobber_action(state, gray_frame)
        state.put_meta('bobber_area', bobber_area)
        return state.set_next_action(Action.WAITING_FOR_A_NIBBLE)

    elif state.action == Action.WAITING_FOR_A_NIBBLE:
        # ждём клёва
        nibble_tick_counter = state.fetch_meta('nibble_tick_counter', 0)
        bobber_area = state.fetch_meta('bobber_area')
        move_to_next_action = _wait_for_nibble_action(state, gray_frame, bobber_area)
        logging.info(f'{move_to_next_action=}')

        if move_to_next_action:
            state.reset()
            return state.set_next_action(Action.HOOKING_THE_FISH)

        else:
            assert nibble_tick_counter <= settings.FISHING_MAX_NIBBLE_WAIT_TICKS, f'Wait nibble timeout {nibble_tick_counter=}'
            state.put_meta('nibble_tick_counter', nibble_tick_counter + 1)
            return state.set_next_action(state.action)

    elif state.action == Action.HOOKING_THE_FISH:
        # подсекаем рыбу
        _hooking_the_fish_action(state, gray_frame)
        return state.reset()


def locations_to_points(locations: ndarray) -> List[Point]:
    return [Point(x=from_x, y=from_y) for from_x, from_y in zip(*locations[::-1])]


def locations_to_center_points(locations: ndarray, template: Point) -> List[Point]:
    return [
        Point(x=from_point.x + int(template.x / 2), y=from_point.y + int(template.y / 2))
        for from_point in locations_to_points(locations)
    ]


def locations_to_areas(locations: ndarray, template: Point) -> List[Area]:
    return [
        Area(
            from_point=from_point,
            to_point=Point(x=from_point.x + template.x, y=from_point.y + template.y)
        )
        for from_point in locations_to_points(locations)
    ]


def show_current_frame(state: State, frame: Union[ScreenShot, ndarray], message: str):
    global DEBUG_FRAMES_COUNTER
    if not state.debug:
        return

    DEBUG_FRAMES_COUNTER += 1

    filepath = str(settings.TMP_FOLDER / f'frame#{DEBUG_FRAMES_COUNTER}-tick#{state.current_tick}-{message}.png')
    if type(frame) is ScreenShot:
        img = Image.frombytes('RGB', frame.size, frame.bgra, 'raw', 'BGRX')
        img.thumbnail((1024, 512))
        img.save(filepath)
    else:
        cv2.imwrite(filepath, frame)

    logging.debug(f'screenshot saved to {filepath=}: {message}')


def _init_action(state: State, gray_frame: ndarray):
    # ищем персонажа
    character_coords = _search_character(state, gray_frame)
    logging.info(f'found character coords {character_coords}')
    assert character_coords, 'Character not found'
    character_point = character_coords[0]

    # ищем воду
    water_coords = _search_water_cell(state, gray_frame)
    logging.info(f'found water cell coords {len(water_coords)}')
    assert water_coords, 'Water cells not found'

    # select nearest water cell
    available_water_cells = list(filter(
        lambda p: p.distance(character_point) <= settings.FISHING_DISTANCE,
        water_coords,
    ))
    assert available_water_cells, 'Not found available water cells for fishing'
    logging.info(f'filtering available cell for fishing {len(available_water_cells)}')
    for point in available_water_cells:
        mark_point(gray_frame, point)
    show_current_frame(state, gray_frame, 'available water cells')

    fishing_cell = random.choice(available_water_cells)
    logging.info(f'select cell for click {fishing_cell}')

    # левый клик
    mouse_move_to(fishing_cell)
    left_click(settings.FISHING_CLICK_DURATION)
    mouse_move_to(Point(x=fishing_cell.x + 24, y=fishing_cell.y + 11))

    # Поплавок может появиться не сразу после заброса удочки, потому ждём какое то время для поиска.
    time.sleep(settings.FISHING_BOBBER_SEARCH_DELAY)

    show_current_frame(state, gray_frame, 'waiting for a nibble')


def _wait_for_bobber_action(state: State, gray_frame: ndarray) -> Area:
    # ищем персонажа
    character_coords = _search_character(state, gray_frame)
    logging.info(f'found character coords {character_coords}')
    assert character_coords, 'Character not found'
    character_point = character_coords[0]

    # ищем поплавок
    bobber_areas = _search_bobber(state, gray_frame, character_point)
    logging.info(f'found bobbers {bobber_areas=}')
    assert bobber_areas, 'Not found bobber'
    return bobber_areas[0]


def _wait_for_nibble_action(state: State, gray_frame: ndarray, bobber_area: Area) -> bool:
    # расширяем зону поиска попловка на который клюнула рыба
    search_area = bobber_area.expand(settings.FISHING_BOBBER_SEARCH_ZONE_OFFSET, settings.FISHING_BOBBER_SEARCH_ZONE_OFFSET)
    logging.debug(f'{search_area=}')

    # ищем поплавок в подводном положении в заданой области экрана
    need_hooking_the_fish = _looking_for_nibbles(state, gray_frame, search_area)
    logging.info(f'{need_hooking_the_fish=}')
    if need_hooking_the_fish:
        left_click(settings.FISHING_CLICK_DURATION)

    return need_hooking_the_fish


def _hooking_the_fish_action(state: State, gray_frame: ndarray) -> bool:
    raise NotImplementedError()
    # todo ищем поплавок-ползунок
    # todo кликаем если отклонился от середины влево
    # todo некликаем если отклонился от середины вправо
    # todo ждём пока он пропадёт


def _search_water_cell(state: State, gray_frame: ndarray) -> List[Point]:
    show_current_frame(state, gray_frame, 'search water cell')

    tpl = templates_client.water_template
    tpl_width, tpl_height = tpl.shape[::-1]
    tpl_point = Point(x=tpl_width, y=tpl_height)

    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.7)

    center_points = locations_to_center_points(loc, tpl_point)
    tmp_frame = copy.copy(gray_frame)
    for point in center_points:
        mark_point(tmp_frame, point)
    show_current_frame(state, tmp_frame, 'search water cells')

    return center_points


def _search_character(state: State, gray_frame: ndarray) -> List[Point]:
    """Ищем координаты персонажа."""
    show_current_frame(state, gray_frame, 'search character')

    tpl = templates_client.character_template
    tpl_width, tpl_height = tpl.shape[::-1]
    tpl_point = Point(x=tpl_width, y=tpl_height)

    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.8)

    characters = locations_to_areas(loc, tpl_point)
    for character_area in characters:
        mark_area(gray_frame, character_area)
    show_current_frame(state, gray_frame, 'search character match')

    center_points = locations_to_center_points(loc, tpl_point)
    for point in center_points:
        mark_point(gray_frame, point)
    show_current_frame(state, gray_frame, 'search character coords')

    return center_points


def _search_bobber(state: State, gray_frame: ndarray, character_point: Point) -> List[Area]:
    """Ищем поплавок на воде."""

    show_current_frame(state, gray_frame, 'search bobber')

    tpl = templates_client.bobber_template
    tpl_width, tpl_height = tpl.shape[::-1]
    tpl_point = Point(x=tpl_width, y=tpl_height)

    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.6)

    tmp_frame = copy.deepcopy(gray_frame)
    areas = locations_to_areas(loc, tpl_point)
    for area in areas:
        mark_area(tmp_frame, area)
    show_current_frame(state, tmp_frame, 'search bobber cells')

    # выбираем ближайший к нам поплавок
    nearest_areas = sorted(areas, key=lambda x: x.center_point.distance(character_point))
    logging.debug(f'rubbers by distance from character {nearest_areas=}')
    show_current_frame(state, tmp_frame, 'filter nearest bobber')

    return nearest_areas


def _looking_for_nibbles(state: State, gray_frame: ndarray, search_area: Area = None) -> bool:
    """Определяем, клюёт ли в данный момент."""

    show_current_frame(state, gray_frame, 'search nibbles')

    if search_area:
        # crop frame to search_area
        gray_frame = gray_frame[search_area.from_point.y:search_area.to_point.y, search_area.from_point.x:search_area.to_point.x]
        show_current_frame(state, gray_frame, 'search nibbles area')
    
    processed_image = cv2.Canny(gray_frame, threshold1=100, threshold2=10)
    show_current_frame(state, processed_image, 'search nibbles Canny')

    mean = np.mean(processed_image)
    median = np.median(processed_image)
    count_non_black_pixels = np.sum(processed_image > 0)
    black_white = np.sum(processed_image > 0) / np.sum(processed_image == 0)

    print(f'np {median=} {mean=} {count_non_black_pixels=} {black_white=}')
    logging.debug(f'looking for nibbles params {median=} {mean=} {count_non_black_pixels=} {black_white=}')
    return black_white >= 0.22
