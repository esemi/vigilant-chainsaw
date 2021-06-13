import pytest

from bot.state import State


@pytest.fixture
def fixture_farm_state() -> State:
    yield State(debug=True, current_tick=0)


@pytest.fixture(autouse=True)
def mock_left_click(mocker):
    import pyautogui

    mocker.patch.object(pyautogui, 'mouseUp', return_value=None)
    mocker.patch.object(pyautogui, 'sleep', return_value=None)
    yield mocker.patch.object(pyautogui, 'mouseDown', return_value=None)
