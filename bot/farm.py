import copy
import logging
import time
from collections import Counter
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Optional, Union, Tuple

import cv2
import mss as mss
import numpy
import numpy as np
from PIL import Image
from mss.models import Monitor
from mss.screenshot import ScreenShot
from numpy import ndarray, int64

# todo sigint handle


DEBUG_FRAMES_COUNTER = 0


@dataclass
class Point:
    x: int64
    y: int64

    @property
    def coords(self) -> Tuple[int, int]:
        return self.x, self.y


class Templates:
    def __init__(self):
        self._folder = Path('../data/templates/')
        assert self._folder.exists()

        self._water = cv2.imread(str(self._folder / 'water.png'), cv2.IMREAD_GRAYSCALE)
        self._character = cv2.imread(str(self._folder / 'character.png'), cv2.IMREAD_GRAYSCALE)

    @property
    def water_template(self) -> ndarray:
        """Шаблон клетки с водой для поиска места для рыбалки."""
        return copy.deepcopy(self._water)

    @property
    def character_template(self) -> ndarray:
        """Шаблон клетки с персонажем."""
        return copy.deepcopy(self._character)


class Action(int, Enum):
    INIT = auto()
    WAITING_FOR_A_NIBBLE = auto()
    HOOKING_THE_FISH = auto()


@dataclass
class State:
    current_iteration: int = 0
    action: Action = Action.INIT
    debug: bool = False

    def set_next_action(self, next_action: Action) -> Action:
        self.action = next_action
        return next_action

    def skip_to_init(self) -> Action:
        self.action = Action.INIT
        return self.action


def select_monitor(sct) -> Monitor:
    return sct.monitors[-1]


def show_current_frame(state: State, frame: Union[ScreenShot, ndarray], message: str):
    global DEBUG_FRAMES_COUNTER
    if not state.debug:
        return

    DEBUG_FRAMES_COUNTER += 1

    debug_folder = Path('../data/debug/')
    filepath = str(debug_folder / f'frame#{DEBUG_FRAMES_COUNTER}-tick#{state.current_iteration}-{message}.png')
    if type(frame) is ScreenShot:
        img = Image.frombytes('RGB', frame.size, frame.bgra, 'raw', 'BGRX')
        img.thumbnail((1024, 512))
        img.save(filepath)
    else:
        cv2.imwrite(filepath, frame)

    logging.debug(message)


def mark_templates(frame: ndarray, loc: tuple, tpl: ndarray):
    w, h = tpl.shape[::-1]
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)


def mark_coords(frame: ndarray, point: Point):
    cv2.circle(frame, point.coords, radius=5, color=(0, 255, 0), thickness=3)


def _search_character(state: State, templates: Templates, gray_frame) -> Point:
    """Ищем координаты персонажа."""
    show_current_frame(state, gray_frame, 'search character')

    tpl = templates.character_template
    res = cv2.matchTemplate(gray_frame, tpl, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.8)
    mark_templates(gray_frame, loc, tpl)
    show_current_frame(state, gray_frame, 'search character match')
    assert loc[0].size
    tpl_width, tpl_height = tpl.shape[::-1]
    character_center_point = Point(x=loc[1][0] + int(tpl_width / 2), y=loc[0][0] + int(tpl_height / 2))
    mark_coords(gray_frame, character_center_point)
    show_current_frame(state, gray_frame, 'search character coords')
    return character_center_point


def _tick_strategy(sct, state: State, templates: Templates) -> Action:
    logging.debug('tick %d %s', state.current_iteration, state)

    monitor = select_monitor(sct)
    screenshot = sct.grab(monitor)
    show_current_frame(state, screenshot, 'init screen')

    source_frame = numpy.array(screenshot)
    gray_frame = cv2.cvtColor(source_frame, cv2.COLOR_BGR2GRAY)
    show_current_frame(state, gray_frame, 'init screen gray')

    character_coords = _search_character(state, templates, gray_frame)

    if state.action == Action.INIT:
        # кликаем по воде удочкой

        # todo ищем ближайшую воду по цвету
        res = cv2.matchTemplate(gray_frame, templates.water_template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.7)
        w, h = templates.water_template.shape[::-1]
        for pt in zip(*loc[::-1]):
            cv2.rectangle(gray_frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
        show_current_frame(state, gray_frame, 'init action template matching')

        # todo левый клик

        return state.set_next_action(Action.WAITING_FOR_A_NIBBLE)

    elif state.action == Action.WAITING_FOR_A_NIBBLE:
        #     ждём клёва

        # todo ищем поплавок
        # todo ждём пока он пропадёт
        # todo левый клик

        return state.set_next_action(Action.HOOKING_THE_FISH)

    elif state.action == Action.HOOKING_THE_FISH:
        # подсекаем рыбу

        # todo ищем поплавок-ползунок
        # todo кликаем если отклонился от середины влево
        # todo некликаем если отклонился от середины вправо
        # todo ждём пока он пропадёт

        return state.skip_to_init()


def farm_bot(
        debug_mode: bool = False,
        limit_iterations: Optional[int] = 5,
        start_delay: int = 5,
) -> Counter:
    counter = Counter()
    state = State(debug=debug_mode)
    templates = Templates()
    logging.info(f'farm bot on {limit_iterations=} {start_delay=}')
    time.sleep(start_delay)
    with mss.mss() as sct:
        while state.current_iteration < limit_iterations or limit_iterations is None:
            state.current_iteration += 1
            counter['last_iteration'] = state.current_iteration

            next_action = _tick_strategy(sct, state, templates)
            logging.info('tick complete %s', next_action)

    logging.info(f'farm bot off {counter=}')
    return counter


if __name__ == '__main__':
    # todo click parse cli options
    debug = True
    max_iterations = 1
    start_delay_sec = 5
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    cnt = farm_bot(debug_mode=debug, limit_iterations=max_iterations, start_delay=start_delay_sec)
    logging.info(cnt)
