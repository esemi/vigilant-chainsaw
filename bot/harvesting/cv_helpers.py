"""Хелперы для работы на стыке с CV."""

import copy
import logging
import random
from typing import List

import cv2  # type: ignore
import numpy as np
from numpy import ndarray

from bot import cv_operations, templates
from bot.gui import Area, Point
from bot.resources import Resources
from bot.state import State


def search_resource(state: State, color_frame: ndarray, resource: Resources) -> List[Point]:
    """Ищем поплавок в миниигре."""
    cv_operations.show_current_frame(state, color_frame, 'search resource frame')

    basic_templates = templates.client.resource(resource.name, level=1)
    source_areas = _search_resource_area(state, color_frame, basic_templates)
    logging.debug('found basic resource areas %s', source_areas)

    first_filter_templates = templates.client.resource(resource.name, level=2)
    filtered_areas = _filter_area_by_templates(state, color_frame, first_filter_templates, source_areas)
    logging.debug('filtered resource areas %s', filtered_areas)

    return list(map(lambda area: area.center_point, filtered_areas))


def choice_cell_for_harvesting(state: State, frame: ndarray, resource_cells: List[Point]) -> Point:
    assert resource_cells, 'Not found resource cells for harvesting'
    cell = random.choice(resource_cells)

    cv_operations.mark_point_group(frame, [cell])
    cv_operations.show_current_frame(state, frame, 'choice_cell_for_harvesting')
    return cell


def _search_resource_area(state: State, frame: ndarray, resource_templates: List[ndarray]) -> List[Area]:
    """Ищем общие патерны ресурса на кадре."""
    areas = []
    for tpl in resource_templates:
        areas.extend(
            _search_template_on_frame(frame, tpl, float(0.45)),  # noqa: WPS432
        )

    tmp_frame = copy.copy(frame)
    cv_operations.mark_area_group(tmp_frame, areas)
    cv_operations.show_current_frame(state, tmp_frame, 'search resource level 1')
    return areas


def _filter_area_by_templates(
    state: State,
    frame: ndarray,
    filter_templates: List[ndarray],
    areas: List[Area],
) -> List[Area]:
    """Фильтруем зоны по найденному внутри оной уточняющему шаблону."""
    filtered_areas = []
    for area in areas:
        area_frame = cv_operations.crop_frame(frame, area)
        for tpl in filter_templates:
            if _search_template_on_frame(area_frame, tpl, float(0.6)):   # noqa: WPS432
                filtered_areas.append(area)
                break

    tmp_frame = copy.copy(frame)
    cv_operations.mark_area_group(tmp_frame, filtered_areas)
    cv_operations.show_current_frame(state, tmp_frame, 'filtering resource areas')
    return filtered_areas


def _search_template_on_frame(frame: ndarray, tpl: ndarray, sensitivity: float) -> List[Area]:
    res = cv2.matchTemplate(frame, tpl, cv2.TM_CCOEFF_NORMED)
    return cv_operations.locations_to_areas(
        np.where(res >= sensitivity),  # noqa: WPS432
        cv_operations.template_to_point(tpl),
    )
