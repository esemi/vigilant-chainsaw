"""Реализация всех возможных стратегий алгоритма фарма конкретного ресурса."""

import logging
from typing import List

from numpy import ndarray

from bot.resources import Resources
from bot.gui import Point
from bot.harvesting import cv_helpers
from bot.state import State


def init_harvesting(state: State, color_frame: ndarray, resource: Resources) -> List[Point]:
    # ищем ресурс на экране
    resource_points = cv_helpers.search_resource(state, color_frame, resource)
    logging.debug('found resource %s coords %s', (resource.name(), resource_points))
    return resource_points
