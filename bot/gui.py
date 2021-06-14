"""Методы и объекты для работы с GUI пользователя."""

import logging
import math
import random
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
        half_size_x = math.floor(self.size.x / 2)
        half_size_y = math.floor(self.size.y / 2)
        return Point(
            self.from_point.x + half_size_x,
            self.from_point.y + half_size_y,
        )

    @property
    def size(self) -> Point:
        return Point(
            self.to_point.x - self.from_point.x,
            self.to_point.y - self.from_point.y,
        )

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
    wait_sec(duration)
    pyautogui.mouseUp(button=pyautogui.LEFT)
    logging.debug('click end')


def wait_sec(duration: float):
    pyautogui.sleep(duration)


def random_point() -> Point:
    return Point(random.randint(10, 100), random.randint(10, 100))
