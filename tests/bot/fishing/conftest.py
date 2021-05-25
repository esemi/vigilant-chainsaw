from pathlib import Path

import pytest

from bot.state import State


@pytest.fixture(scope="module")
def screenshots_dir() -> Path:
    folder = Path(__file__).parent.joinpath('./screenshots/')
    assert folder.exists()
    yield folder


@pytest.fixture(scope="module")
def fixture_farm_state() -> State:
    yield State(debug=True, current_tick=0)
