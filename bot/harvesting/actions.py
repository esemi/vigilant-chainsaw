"""Реализация всех возможных стратегий алгоритма фарма конкретного ресурса."""

import logging
from typing import List

from numpy import ndarray

from bot import gui, settings
from bot.harvesting import cv_helpers
from bot.resources import Resources
from bot.state import State


def init_harvesting(state: State, color_frame: ndarray, resource: Resources) -> List[gui.Point]:
    # ищем ресурс на экране
    resource_points = cv_helpers.search_resource(state, color_frame, resource)
    logging.debug('found resource %s coords %s', resource.name, resource_points)
    return resource_points


def harvest(state: State, color_frame: ndarray, points: List[gui.Point]):
    selected_point = cv_helpers.choice_cell_for_harvesting(state, color_frame, points)
    logging.debug('harvest cell=%s', selected_point)

    gui.mouse_move_to(selected_point, float(1))
    gui.left_click(settings.HARVESTING_CLICK_DURATION)
    gui.wait_sec(settings.HARVESTING_PAUSE)
    gui.mouse_move_to(gui.random_point(), float(2))
