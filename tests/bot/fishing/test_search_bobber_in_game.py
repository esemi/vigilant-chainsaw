import cv2
import numpy
import pytest
from pytest_cases import parametrize

from bot.fishing.cv_helpers import search_bobber_in_game
from bot.state import State
from tests.bot.fishing.conftest import bobber_game_left_side_templates, bobber_game_templates, bobber_templates


@parametrize('filepath', bobber_templates())
def test_false_positive(fixture_farm_state: State, filepath: str):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)

    res = search_bobber_in_game(fixture_farm_state, gray_frame)

    assert not res


@pytest.mark.parametrize('filepath', bobber_game_left_side_templates() + bobber_game_templates())
def test_bobber_in_left_or_center_position(fixture_farm_state: State, filepath: str):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)

    res = search_bobber_in_game(fixture_farm_state, gray_frame)

    assert res
