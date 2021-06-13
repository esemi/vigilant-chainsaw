"""Хелперы для работы на стыке с CV."""

import copy
from typing import List

import cv2  # type: ignore
import numpy as np
from PIL import Image  # type: ignore
from mss.screenshot import ScreenShot  # type: ignore
from numpy import ndarray

from bot import cv_operations, templates
from bot.resources import Resources
from bot.gui import Point
from bot.state import State


def search_resource(state: State, color_frame: ndarray, resource: Resources) -> List[Point]:
    """Ищем поплавок в миниигре."""

    center_points = []

    cv_operations.show_current_frame(state, color_frame, 'search resource frame')
    for tpl in templates.client.resource(resource.name):
        res = cv2.matchTemplate(color_frame, tpl, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= float(0.65))  # noqa: WPS432
        center_points += cv_operations.locations_to_center_points(
            loc,
            cv_operations.template_to_point(tpl),
        )

        areas = cv_operations.locations_to_areas(
            loc,
            cv_operations.template_to_point(tpl),
        )
        cv_operations.mark_area_group(color_frame, areas)

    cv_operations.show_current_frame(state, color_frame, 'search resource %s cells' % resource.name)

    return center_points
