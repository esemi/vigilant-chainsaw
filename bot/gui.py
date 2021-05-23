import logging
import math
from dataclasses import dataclass
from typing import Tuple

import pyautogui


@dataclass
class Point:
    x: int
    y: int

    @property
    def coords(self) -> Tuple[int, int]:
        return self.x, self.y

    def distance(self, to: 'Point') -> float:
        return math.hypot(to.x - self.x, to.y - self.y)


@dataclass
class Area:
    from_point: Point
    to_point: Point


def mouse_move_to(point: Point, duration: float = 0.6):
    logging.debug(f'mouse move {point=}')
    pyautogui.moveTo(point.x, point.y, duration=duration, tween=pyautogui.easeOutQuad)
    logging.debug('mouse moved')


def left_click(duration: float):
    logging.debug('click start')
    pyautogui.mouseDown(button=pyautogui.LEFT)
    pyautogui.sleep(duration)
    pyautogui.mouseUp(button=pyautogui.LEFT)
    logging.debug('click end')

