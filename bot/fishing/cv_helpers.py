"""Хелперы для работы на стыке с CV."""

import copy
import logging
import random
from typing import List

import cv2  # type: ignore
import numpy as np
from PIL import Image  # type: ignore
from mss.screenshot import ScreenShot  # type: ignore
from numpy import ndarray

from bot import cv_operations, settings, templates
from bot.gui import Area, Point, sort_areas_by_distance
from bot.state import State


def search_water_cell(state: State, gray_frame: ndarray) -> List[Point]:
    cv_operations.show_current_frame(state, gray_frame, 'search water cell')

    tpl = templates.client.water_template

    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= float(0.7))  # noqa: WPS432

    center_points = cv_operations.locations_to_center_points(
        loc,
        cv_operations.template_to_point(tpl),
    )
    tmp_frame = copy.copy(gray_frame)
    cv_operations.mark_point_group(tmp_frame, center_points)
    cv_operations.show_current_frame(state, tmp_frame, 'search water cells')

    return center_points


def choice_cell_for_fishing(state: State, gray_frame: ndarray, character: Point, water_cells: List[Point]) -> Point:
    available_water_cells = list(filter(
        lambda cell: settings.FISHING_DISTANCE_MIN < cell.distance(character) < settings.FISHING_DISTANCE_MAX,
        water_cells,
    ))
    assert available_water_cells, 'Not found available water cells for fishing'
    logging.debug('filtering available cell for fishing %s', len(available_water_cells))
    cv_operations.mark_point_group(gray_frame, available_water_cells)
    cv_operations.show_current_frame(state, gray_frame, 'choice cell for fishing')

    return random.choice(available_water_cells)


def search_character(state: State, gray_frame: ndarray) -> List[Point]:
    """Ищем координаты персонажа."""
    cv_operations.show_current_frame(state, gray_frame, 'search character')

    tpl_point = cv_operations.template_to_point(templates.client.character_template)

    res = cv2.matchTemplate(gray_frame, templates.client.character_template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= float(0.8))  # noqa: WPS432

    characters = cv_operations.locations_to_areas(loc, tpl_point)
    cv_operations.mark_area_group(gray_frame, characters)
    cv_operations.show_current_frame(state, gray_frame, 'search character match')

    return cv_operations.locations_to_center_points(loc, tpl_point)


def search_bobber(state: State, gray_frame: ndarray, character: Point) -> List[Area]:
    """Ищем поплавок на воде."""
    tpl = templates.client.bobber_template

    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= float(0.55))  # noqa: WPS432
    areas = cv_operations.locations_to_areas(
        loc,
        cv_operations.template_to_point(tpl),
    )

    tmp_frame = copy.deepcopy(gray_frame)
    cv_operations.mark_area_group(tmp_frame, areas)
    cv_operations.show_current_frame(state, tmp_frame, 'search bobber cells')

    return sort_areas_by_distance(areas, character)


def lookup_hooking_game_area(state: State, gray_frame: ndarray) -> List[Area]:
    """Ищем миниигру."""
    tpl = templates.client.hooking_game_template

    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= float(0.6))  # noqa: WPS432
    areas = cv_operations.locations_to_areas(
        loc,
        cv_operations.template_to_point(tpl),
    )

    cv_operations.mark_area_group(gray_frame, areas)
    cv_operations.show_current_frame(state, gray_frame, 'lookup game area')

    return areas


def looking_for_nibbles(state: State, gray_frame: ndarray, search_area: Area) -> bool:
    """Определяем, клюёт ли в данный момент."""
    # crop frame to search_area
    gray_frame = cv_operations.crop_frame(gray_frame, search_area)
    cv_operations.show_current_frame(state, gray_frame, 'search nibbles area')

    processed_image = cv2.Canny(gray_frame, threshold1=35, threshold2=15)  # noqa: WPS432
    cv_operations.show_current_frame(state, processed_image, 'search nibbles Canny')
    black_count = np.sum(processed_image == 0)
    bw_factor = np.count_nonzero(processed_image) / black_count
    logging.info('black vs white factor: %s', bw_factor)

    return bw_factor >= settings.FISHING_NIBBLES_THRESHOLD


def search_bobber_in_game(state: State, gray_frame: ndarray) -> List[Point]:
    """Ищем поплавок в миниигре."""
    tpl = templates.client.bobber_in_game_template

    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= float(0.6))  # noqa: WPS432
    return cv_operations.locations_to_center_points(
        loc,
        cv_operations.template_to_point(tpl),
    )
