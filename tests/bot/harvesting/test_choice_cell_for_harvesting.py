import cv2
import numpy
import pytest

from bot import resources
from bot.gui import Point
from bot.harvesting.cv_helpers import choice_cell_for_harvesting, search_resource
from bot.state import State
from tests.bot.harvesting.conftest import cotton_templates


@pytest.mark.parametrize('filepath', cotton_templates())
def test_smoke(fixture_farm_state: State, filepath: str):
    screenshot = cv2.imread(filepath, cv2.IMREAD_COLOR)
    frame = numpy.array(screenshot)
    points = search_resource(fixture_farm_state, frame, resources.Resources.COTTON)

    res = choice_cell_for_harvesting(fixture_farm_state, frame, points)
    res2 = choice_cell_for_harvesting(fixture_farm_state, frame, points)
    assert isinstance(res, Point)
    assert res.coords != res2.coords

