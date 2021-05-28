from unittest.mock import MagicMock

import cv2
import numpy
import pytest

from bot.fishing.actions import hooking_the_fish_action
from bot.fishing.cv_helpers import lookup_hooking_game_area
from bot.gui import Area, Point
from bot.state import State
from tests.bot.fishing.conftest import bobber_game_left_side_templates, bobber_game_templates, bobber_game_right_side_templates, bobber_templates


@pytest.mark.parametrize('filepath', bobber_game_templates())
def test_bobber_in_center(fixture_farm_state: State, filepath: str, mock_left_click: MagicMock):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)
    area = lookup_hooking_game_area(fixture_farm_state, gray_frame)[0]

    res = hooking_the_fish_action(fixture_farm_state, gray_frame, area)

    # check click not called
    mock_left_click.assert_not_called()

    assert not res


@pytest.mark.parametrize('filepath', bobber_game_left_side_templates())
def test_bobber_in_left(fixture_farm_state: State, filepath: str, mock_left_click: MagicMock):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)
    game_area = Area(from_point=Point(1018, 554), to_point=Point(1173, 574))

    res = hooking_the_fish_action(fixture_farm_state, gray_frame, game_area)

    # check click called
    mock_left_click.assert_called_once()

    assert not res


@pytest.mark.parametrize('filepath', bobber_game_right_side_templates())
def test_bobber_in_right(fixture_farm_state: State, filepath: str, mock_left_click: MagicMock):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)
    game_area = Area(from_point=Point(x=1172, y=557), to_point=Point(x=1327, y=577))

    res = hooking_the_fish_action(fixture_farm_state, gray_frame, game_area)

    # check click called
    mock_left_click.assert_not_called()

    assert not res


@pytest.mark.parametrize('filepath', bobber_templates())
def test_bobber_not_found(fixture_farm_state: State, filepath: str, mock_left_click: MagicMock):
    screenshot = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    gray_frame = numpy.array(screenshot)
    game_area = Area(from_point=Point(1018, 554), to_point=Point(1173, 574))

    res = hooking_the_fish_action(fixture_farm_state, gray_frame, game_area)

    # check click called
    mock_left_click.assert_not_called()

    assert res
