"""Методы работы с библиотекой для CV."""
import logging
from typing import List, Union

import cv2  # type: ignore
from PIL import Image  # type: ignore
from mss.screenshot import ScreenShot  # type: ignore
from numpy import ndarray

from bot import settings
from bot.color import Color
from bot.gui import Area, Point
from bot.state import State


def mark_area_group(frame: ndarray, areas: List[Area], color: Color = Color.BLACK):
    for area in areas:
        from_point, to_point = area.astuple()
        cv2.rectangle(frame, from_point.coords, to_point.coords, color=color.value, thickness=1)


def mark_point_group(frame: ndarray, points: List[Point], color: Color = Color.BLACK):
    for point in points:
        cv2.circle(frame, point.coords, radius=5, color=color.value, thickness=2)


def _locations_to_points(locations: ndarray) -> List[Point]:
    return [
        Point(x=from_x, y=from_y)
        for from_x, from_y in zip(*locations[::-1])
    ]


def locations_to_center_points(locations: ndarray, template: Point) -> List[Point]:
    return [
        Point(
            x=from_point.x + int(template.x / 2),
            y=from_point.y + int(template.y / 2),
        ) for from_point in _locations_to_points(locations)
    ]


def locations_to_areas(locations: ndarray, template: Point) -> List[Area]:
    return [
        Area(
            from_point=from_point,
            to_point=Point(
                x=from_point.x + template.x,
                y=from_point.y + template.y,
            ),
        )
        for from_point in _locations_to_points(locations)
    ]


def template_to_point(template: ndarray) -> Point:
    return Point(template.shape[1], template.shape[0])


def crop_frame(frame: ndarray, area: Area) -> ndarray:
    from_, to = area.from_point, area.to_point
    return frame[from_.y:to.y, from_.x:to.x]


DEBUG_FRAMES_COUNTER = 0


def show_current_frame(state: State, frame: Union[ScreenShot, ndarray], message: str, force: bool = False):
    global DEBUG_FRAMES_COUNTER  # noqa: WPS420

    DEBUG_FRAMES_COUNTER += 1

    if not state.debug and not force:
        return

    filename = f'frame#{DEBUG_FRAMES_COUNTER}-tick#{state.current_tick}-{message}.png'  # noqa: WPS305
    filepath = str(settings.TMP_FOLDER / filename)
    if isinstance(frame, ScreenShot):
        img = Image.frombytes('RGB', frame.size, frame.bgra, 'raw', 'BGRX')
        img.thumbnail((1024, 512))
        img.save(filepath)
    else:
        cv2.imwrite(filepath, frame)
    logging.info('screenshot saved to %s: %s', str(filepath), message)
