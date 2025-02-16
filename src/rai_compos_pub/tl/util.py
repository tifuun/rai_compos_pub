"""tl/util.py -- supporting classes and functions for TL"""

from enum import Enum

import raimad as rai

class TurnDirection(Enum):
    AROUND = -1
    STRAIGHT = 0
    LEFT = 1
    RIGHT = 2

class Orientation(Enum):
    CLOCKWISE = -1
    COUNTERCLOCKWISE = 1

def cross2d(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def classify_turn(before, point, after):
    # Thank you ChatGPT for this one,
    # it seems the day has come when AI
    # understands linear algebra better than I do
    prod = cross2d(
        rai.sub(point, before),
        rai.sub(after, point)
        )
    # TODO some way to flatten this?

    if abs(prod) < 0.01:  # TODO epsilon
        return TurnDirection.STRAIGHT
    if prod > 0:
        return TurnDirection.LEFT
    elif prod < 0:
        return TurnDirection.RIGHT

    # TODO turns around

def format_path(path):
    return '\n'.join([*[repr(conn) for conn in path], '\n'])

