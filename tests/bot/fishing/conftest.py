from pathlib import Path
from typing import List

import pytest

from bot.state import State


def screenshots_dir() -> Path:
    folder = Path(__file__).parent.joinpath('./screenshots/')
    assert folder.exists()
    return folder


@pytest.fixture
def fixture_farm_state() -> State:
    yield State(debug=True, current_tick=0)


def nibbles_templates() -> List[str]:
    return [str(screenshots_dir() / i) for i in ['nibble_1.png', 'nibble_2.png', 'nibble_3.png', 'nibble_4.png']]


def bobber_templates() -> List[str]:
    return [str(screenshots_dir() / i) for i in ['bobber_1.png', 'bobber_2.png']]


def bobber_game_templates() -> List[str]:
    return [str(screenshots_dir() / i) for i in ['bobber_game_1.png', 'bobber_game_2.png']]


def bobber_game_left_side_templates() -> List[str]:
    folder = screenshots_dir() / 'bobber_game_left'
    return [str(filename) for filename in folder.glob('*.png') if filename.is_file()]


def bobber_game_right_side_templates() -> List[str]:
    folder = screenshots_dir() / 'bobber_game_right'
    return [str(filename) for filename in folder.glob('*.png') if filename.is_file()]


@pytest.fixture(autouse=True)
def mock_left_click(mocker):
    import pyautogui

    mocker.patch.object(pyautogui, 'mouseUp', return_value=None)
    mocker.patch.object(pyautogui, 'sleep', return_value=None)
    yield mocker.patch.object(pyautogui, 'mouseDown', return_value=None)
