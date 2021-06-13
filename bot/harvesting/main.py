"""Верхнеуровневая реализцация бота по максимально простому сбору ресурсов на экране."""
import logging
import time

import cv2  # type: ignore
import numpy
from mss.screenshot import ScreenShot  # type: ignore

from bot import cv_operations
from bot.harvesting import actions
from bot.resources import Resources
from bot.state import Action, State


def tick(screenshot: ScreenShot, state: State, resource: Resources = Resources.COTTON) -> Action:  # noqa: WPS231; WPS223
    """Фармим ресурс.

    - ищем все клетки с ресурсами
    - кликаем на рандомный из них
    - делаем паузу для сбора
    - повторяем

    INIT -> HARVEST

    """
    color_frame = numpy.array(screenshot)
    cv_operations.show_current_frame(state, color_frame, 'init screen')

    if state.action == Action.INIT:
        # ищем ресурсы для сбора
        state.meta.target_points = actions.init_harvesting(state, color_frame, resource)
        if not state.meta.target_points:
            logging.info('not found resource for harvesting')
            time.sleep(5)
            return Action.INIT
        return state.set_next_action(Action.HARVEST)

    if state.action == Action.HARVEST:
        # выбираем цель и собираем
        assert state.meta.target_points
        actions.harvest(state, color_frame, state.meta.target_points)
        return state.set_next_action(Action.INIT)

    raise NotImplementedError()
