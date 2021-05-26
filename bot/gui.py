"""Методы и объекты для работы с GUI пользователя."""

import logging
import math
from dataclasses import dataclass
from typing import List, Tuple

import pyautogui  # type: ignore


@dataclass
class Point(object):
    x: int  # noqa: WPS111
    y: int  # noqa: WPS111

    @property
    def coords(self) -> Tuple[int, int]:
        return self.x, self.y

    def distance(self, to: 'Point') -> float:
        return math.hypot(to.x - self.x, to.y - self.y)


@dataclass
class Area(object):
    from_point: Point
    to_point: Point

    @property
    def center_point(self) -> Point:
        point_x = (self.to_point.x - self.from_point.x) / 2
        point_y = (self.to_point.y - self.from_point.y) / 2
        return Point(x=int(point_x), y=int(point_y))

    def astuple(self) -> Tuple[Point, Point]:
        return self.from_point, self.to_point


def sort_areas_by_distance(areas: List[Area], target: Point) -> List[Area]:
    sorted_areas = sorted(areas, key=lambda area: area.center_point.distance(target))
    logging.debug('rubbers by distance from character %s', sorted_areas)
    return sorted_areas


def mouse_move_to(point: Point, duration: float = 0.6):
    logging.debug('mouse move %s', point)
    pyautogui.moveTo(point.x, point.y, duration=duration, tween=pyautogui.easeOutQuad)
    logging.debug('mouse moved')


def left_click(duration: float):
    logging.debug('click start')
    pyautogui.mouseDown(button=pyautogui.LEFT)
    pyautogui.sleep(duration)
    pyautogui.mouseUp(button=pyautogui.LEFT)
    logging.debug('click end')
