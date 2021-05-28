import cv2
import numpy
import pytest

from bot.fishing.cv_helpers import search_bobber
from bot.gui import Point
from bot.state import State
from tests.bot.fishing.conftest import bobber_templates, nibbles_templates


@pytest.mark.parametrize('filepath', bobber_templates())
def test_search_bobber_happy_path(fixture_farm_state: State, filepath: str):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)

    res = search_bobber(fixture_farm_state, gray_frame, Point(x=0, y=0))

    assert len(res) > 0


@pytest.mark.parametrize('filepath', nibbles_templates())
def test_search_bobber_false_positive(fixture_farm_state: State, filepath: str):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)

    res = search_bobber(fixture_farm_state, gray_frame, Point(x=0, y=0))

    # поплавок в подводном положении не сильно отличим от надводного
    # в будущем можно исправить эту проблему тем же решением, как в _looking_for_nibbles (через Canny edge selection)
    assert len(res) > 0
