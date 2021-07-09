"""Типы поддерживаемых игровых ресурсов."""

from enum import Enum


class Resources(str, Enum):
    FISH = 'fish'
    COTTON = 'cotton'
