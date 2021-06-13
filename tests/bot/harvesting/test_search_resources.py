import cv2
import numpy
import pytest

from bot import resources
from bot.harvesting.cv_helpers import search_resource
from bot.state import State
from tests.bot.harvesting.conftest import cotton_templates, screenshots_dir

COLOR_SCHEME = cv2.IMREAD_COLOR


@pytest.mark.parametrize('filepath', cotton_templates())
def test_cotton(fixture_farm_state: State, filepath: str):
    screenshot = cv2.imread(filepath, COLOR_SCHEME)
    gray_frame = numpy.array(screenshot)

    res = search_resource(fixture_farm_state, gray_frame, resources.Resources.COTTON)

    assert res


def test_cotton_false_positive(fixture_farm_state: State):
    filepath = str(screenshots_dir() / 'cotton-empty.png')
    screenshot = cv2.imread(filepath, COLOR_SCHEME)
    gray_frame = numpy.array(screenshot)

    points = search_resource(fixture_farm_state, gray_frame, resources.Resources.COTTON)

    assert not points
