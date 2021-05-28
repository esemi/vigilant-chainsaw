import cv2
import numpy
import pytest
from pytest_cases import parametrize

from bot.fishing.cv_helpers import lookup_hooking_game_area
from bot.state import State
from tests.bot.fishing.conftest import bobber_game_templates, nibbles_templates, bobber_templates, bobber_game_left_side_templates


@parametrize('filepath', bobber_game_templates())
def test_lookup_hooking_game_area_happy_path(fixture_farm_state: State, filepath: str):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)

    res = lookup_hooking_game_area(fixture_farm_state, gray_frame)

    assert len(res) > 0


@pytest.mark.parametrize('filepath', nibbles_templates() + bobber_templates())
def test_search_bobber_game_false_positive(fixture_farm_state: State, filepath: str):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)

    res = lookup_hooking_game_area(fixture_farm_state, gray_frame)

    assert not res
