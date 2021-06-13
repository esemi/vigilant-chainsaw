"""Верхнеуровневая реализцация бота."""
import logging

import cv2  # type: ignore
import numpy
from mss.screenshot import ScreenShot  # type: ignore

import bot.cv_operations
from bot import settings
from bot.fishing import actions, cv_helpers
from bot.state import Action, State


def tick(screenshot: ScreenShot, state: State) -> Action:  # noqa: WPS231; WPS223
    """Фармим рыбалку.

    - ищем ближайшую клетку с водой и забрасываем удочку
    - ждём пока поплавок скроется под водой и дёргаем
    - подсекаем рыбу пока миниагра с ползунком не исчезнет
    - повторяем

    INIT
    START_FISHING -> WAITING_FOR_A_RUBBER -> WAITING_FOR_A_NIBBLE -> WAITING_FOR_A_HOOKING_GAME -> HOOKING_THE_FISH

    """
    color_frame = numpy.array(screenshot)
    bot.cv_operations.show_current_frame(state, color_frame, 'init screen')
    gray_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)

    if state.action == Action.INIT:
        # подготовка окружения
        state.meta.target_point = actions.init_action(state, gray_frame)
        return state.set_next_action(Action.START)

    if state.action == Action.START:
        # забрасываем удочку
        assert state.meta.target_point
        actions.start_fishing_action(state, gray_frame, state.meta.target_point)
        return state.set_next_action(Action.WAITING_FOR_A_BOBBER)

    if state.action == Action.WAITING_FOR_A_BOBBER:
        # ждём пока появится поплавок над водой
        state.meta.bobber_area = actions.wait_for_bobber_action(state, gray_frame)
        state.meta.nibble_tick_counter = 0
        logging.info('bobber area saved %s', state.meta.bobber_area)
        return state.set_next_action(Action.WAITING_FOR_A_NIBBLE)

    if state.action == Action.WAITING_FOR_A_NIBBLE:
        # ждём клёва
        assert state.meta.bobber_area
        move_to_next_action = actions.wait_for_nibble_action(
            state,
            gray_frame,
            state.meta.bobber_area,
        )
        if not move_to_next_action:
            assert state.meta.nibble_tick_counter <= settings.FISHING_MAX_NIBBLE_WAIT_TICKS, 'Waiting nibble timeout'
            state.meta.nibble_tick_counter += 1
        return state.set_next_action(Action.WAITING_FOR_A_HOOKING_GAME) if move_to_next_action else state.action

    if state.action == Action.WAITING_FOR_A_HOOKING_GAME:
        # ждём пока миниигра с подсеканием рыбы
        game_area = actions.wait_for_hooking_game_action(state, gray_frame)
        logging.info('game area saved %s', game_area)
        state.meta.game_area = game_area
        return state.set_next_action(Action.HOOKING_THE_FISH)

    if state.action == Action.HOOKING_THE_FISH:
        # играем в подсечку рыбы
        assert state.meta.game_area
        move_to_next_action = actions.hooking_the_fish_action(state, gray_frame, state.meta.game_area)
        return state.set_next_action(Action.START) if move_to_next_action else state.action

    raise NotImplementedError()
