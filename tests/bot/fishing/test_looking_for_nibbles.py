import cv2
import numpy
import pytest

from bot.fishing.cv_helpers import looking_for_nibbles, search_bobber
from bot.gui import Point
from bot.state import State
from tests.bot.fishing.conftest import nibbles_templates, bobber_templates


@pytest.mark.parametrize('filepath', nibbles_templates())
def test_looking_for_nibbles_happy_path_first(fixture_farm_state: State, filepath: str):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)
    area = search_bobber(fixture_farm_state, gray_frame, Point(0, 0))[0]
    assert area

    res = looking_for_nibbles(fixture_farm_state, gray_frame, area)
    assert res


@pytest.mark.parametrize('filepath', bobber_templates())
def test_looking_for_nibbles_false_positive(fixture_farm_state: State, filepath: str):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)
    area = search_bobber(fixture_farm_state, gray_frame, Point(0, 0))[0]
    assert area

    res = looking_for_nibbles(fixture_farm_state, gray_frame, area)
    assert not res
