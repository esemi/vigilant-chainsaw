from pytest_cases import parametrize

from bot.gui import Area, Point


@parametrize('test_area, expected', [
    (Area(Point(0, 0), Point(10, 5)), Point(5, 2)),
    (Area(Point(3, 3), Point(10, 5)), Point(6, 4)),
])
def test_area_center(test_area: Area, expected: Point):
    assert test_area.center_point == expected


@parametrize('test_area, expected', [
    (Area(Point(0, 0), Point(10, 5)), Point(10, 5)),
    (Area(Point(3, 3), Point(10, 5)), Point(7, 2)),
])
def test_area_size(test_area: Area, expected: Point):
    assert test_area.size == expected
