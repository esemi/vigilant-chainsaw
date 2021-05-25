from pathlib import Path

import cv2
import numpy
import pytest

from bot.fishing import _looking_for_nibbles, _search_bobber, show_current_frame
from bot.gui import Point
from bot.state import State


@pytest.mark.parametrize('frame_image_path', ['nibble_1.png', 'nibble_2.png', 'nibble_3.png', 'nibble_4.png'])
def test_looking_for_nibbles_happy_path_first(screenshots_dir: Path, fixture_farm_state: State, frame_image_path: str):
    screenshot = cv2.imread(str(screenshots_dir / frame_image_path), cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)
    area = _search_bobber(fixture_farm_state, gray_frame, Point(0, 0))[0]
    assert area

    show_current_frame(fixture_farm_state, gray_frame, 'debug', True)
    res = _looking_for_nibbles(fixture_farm_state, gray_frame, area)
    # PASSED [ 50%]np median=0.0 mean=55.039970930232556 count_non_black_pixels=297 black_white=0.2752548656163114
    # PASSED [100%]np median=0.0 mean=52.44549418604651 count_non_black_pixels=283 black_white=0.25892040256175664
    assert res


@pytest.mark.parametrize('frame_image_path', ['bobber_1.png', 'bobber_2.png'])
def test_looking_for_nibbles_false_positive(screenshots_dir: Path, fixture_farm_state: State, frame_image_path: str):
    screenshot = cv2.imread(str(screenshots_dir / frame_image_path), cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)
    area = _search_bobber(fixture_farm_state, gray_frame, Point(0, 0))[0]
    assert area

    res = _looking_for_nibbles(fixture_farm_state, gray_frame, area)
    # FAILED [ 50%]np median=0.0 mean=25.388808139534884 count_non_black_pixels=137 black_white=0.11057304277643261
    # FAILED [100%]np median=0.0 mean=28.16860465116279 count_non_black_pixels=152 black_white=0.12418300653594772
    assert not res

