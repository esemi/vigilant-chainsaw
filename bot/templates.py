"""Класс доступа к образцам игровых сущностей."""

import copy
from pathlib import Path
from typing import Dict, List

import cv2  # type: ignore
from numpy import ndarray

from bot import settings


class Templates(object):
    def __init__(self, folder: Path):
        self._folder = folder
        self._water = cv2.imread(str(folder / 'water.png'), cv2.IMREAD_GRAYSCALE)
        self._character = cv2.imread(str(folder / 'character.png'), cv2.IMREAD_GRAYSCALE)
        self._bobber = cv2.imread(str(folder / 'bobber.png'), cv2.IMREAD_GRAYSCALE)
        self._hooking_game = cv2.imread(str(folder / 'hooking_game.png'), cv2.IMREAD_GRAYSCALE)
        self._bobber_in_game = cv2.imread(str(folder / 'bobber_in_game.png'), cv2.IMREAD_GRAYSCALE)
        self._resources: Dict[str, List[ndarray]] = {}

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

    @property
    def hooking_game_template(self) -> ndarray:
        """Шаблон миниигры рыбалки."""
        return copy.deepcopy(self._hooking_game)

    @property
    def bobber_in_game_template(self) -> ndarray:
        """Шаблон поплавка в миниигре."""
        return copy.deepcopy(self._bobber_in_game)

    def resource(self, resource_name: str, level: int = 1) -> List[ndarray]:
        index = '%s-%s' % (resource_name, str(level))
        folder = self._folder / 'resource' / resource_name / ('level%d' % level)

        if index not in self._resources:
            files = [filename for filename in folder.glob('*.png') if filename.is_file()]
            self._resources[index] = [
                cv2.imread(str(folder / filename), cv2.IMREAD_COLOR)
                for filename in files
            ]

        return copy.deepcopy(self._resources[index])


client = Templates(settings.TEMPLATES_FOLDER)
