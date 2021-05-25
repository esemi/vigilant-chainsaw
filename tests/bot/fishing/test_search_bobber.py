from pathlib import Path

import cv2
import numpy
import pytest

from bot.fishing.cv_helpers import search_bobber
from bot.gui import Point
from bot.state import State


@pytest.mark.parametrize('frame_image_path', ['bobber_1.png', 'bobber_2.png'])
def test_search_bobber_happy_path(screenshots_dir: Path, fixture_farm_state: State,
                                  frame_image_path: str):
    screenshot = cv2.imread(str(screenshots_dir / frame_image_path), cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)

    res = search_bobber(fixture_farm_state, gray_frame, Point(x=0, y=0))

    assert len(res) > 0


@pytest.mark.parametrize('frame_image_path', ['nibble_1.png', 'nibble_2.png', 'nibble_3.png', 'nibble_4.png'])
def test_search_bobber_false_positive(screenshots_dir: Path, fixture_farm_state: State,
                                      frame_image_path: str):
    screenshot = cv2.imread(str(screenshots_dir / frame_image_path), cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)

    res = search_bobber(fixture_farm_state, gray_frame, Point(x=0, y=0))

    # поплавок в подводном положении не сильно отличим от надводного
    # в будущем можно исправить эту проблему тем же решением, как в _looking_for_nibbles (через Canny edge selection)
    assert len(res) > 0
