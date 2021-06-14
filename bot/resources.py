"""Типы поддерживаемых игровых ресурсов."""

from enum import Enum, auto


class Resources(int, Enum):
    FISH = auto()
    COTTON = auto()
