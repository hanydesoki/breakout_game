import math

from pygame import Rect


def clamp_value(value: float, minimum: float, maximum: float) -> float:
    return min(maximum, max(minimum, value))


def distance_between_two_points(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def point_in_circle(point: tuple[float, float], center: tuple[float, float], radius: float) -> bool:
    return distance_between_two_points(point, center) < radius


def circle_rectangle_intersection(circle_x: float, circle_y: float, radius: float, rectangle: Rect) -> bool:
    closest_x = clamp_value(circle_x, rectangle.left, rectangle.right)
    closest_y = clamp_value(circle_y, rectangle.top, rectangle.bottom)

    return point_in_circle((closest_x, closest_y), (circle_x, circle_y), radius)


def interpolate_value(a: float, b: float, i: int, n: int) -> float:

    return a + i * (b - a) / n


def color_gradient(color1: tuple[int, int, int],
                   color2: tuple[int, int, int], i: int, n: int) -> tuple:
    new_color = [round(clamp_value(interpolate_value(c1, c2, i, n), 0, 255)) for c1, c2 in zip(color1, color2)]

    return tuple(new_color)
