from typing import Callable

import pytest
from pytest_cases import parametrize

from bot.farm.farm import select_farming_module
from bot.resources import Resources


@parametrize('resource', Resources)
def test_happy_path(resource: Resources):
    res = select_farming_module(resource)
    assert isinstance(res, Callable)


def test_unknown_resource():
    with pytest.raises(NotImplementedError):
        select_farming_module(None)
