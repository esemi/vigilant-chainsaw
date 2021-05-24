import copy
import logging
from pathlib import Path

import cv2
from numpy import ndarray

from bot.gui import Point, Area


class Templates:
    def __init__(self):
        self._folder = Path(__file__).parent.joinpath('../data/templates')
        assert self._folder.exists()

        self._water = cv2.imread(str(self._folder / 'water.png'), cv2.IMREAD_GRAYSCALE)
        self._character = cv2.imread(str(self._folder / 'character.png'), cv2.IMREAD_GRAYSCALE)
        self._bobber = cv2.imread(str(self._folder / 'bobber.png'), cv2.IMREAD_GRAYSCALE)

    @property
    def water_template(self) -> ndarray:
        """Шаблон клетки с водой для поиска места для рыбалки."""
        return copy.deepcopy(self._water)

    @property
    def character_template(self) -> ndarray:
        """Шаблон клетки с персонажем."""
        return copy.deepcopy(self._character)

    @property
    def bobber_template(self) -> ndarray:
        """Шаблон клетки поплавком в надводном положении."""
        return copy.deepcopy(self._bobber)


templates_client = Templates()


def mark_area(frame: ndarray, area: Area):
    cv2.rectangle(frame, area.from_point.coords, area.to_point.coords, (0, 255, 0), 1)


def mark_point(frame: ndarray, point: Point):
    cv2.circle(frame, point.coords, radius=5, color=(0, 255, 0), thickness=2)
