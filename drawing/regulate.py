import random
import math
from .util import pallette


def regulate(output):
    if output.__class__ == list:
        output = keep_tuples(output)
        regulated_output = []
        for forward, turn, width, colour in output:
            forward = regulate_forward(forward)
            turn = regulate_turn(turn)
            width = regulate_width(width)
            colour = regulate_colour(colour)
            regulated_output.append((forward, turn, width, colour))
        output = list(set(regulated_output))
        output = shorten_output(output)
        return output
    else:
        return []


def regulate_colour(colour):
    try:
        return colour % len(pallette)
    except (ValueError, TypeError):
        return 0


def regulate_forward(forward):
    try:
        forward = abs(forward)
        x = 5
        return math.log(forward * x) * math.log(forward * x)
    except (ValueError, TypeError):
        return 5


def regulate_turn(turn):
    if turn.__class__ == int:
        return turn
    else:
        return 0


def regulate_width(width):
    try:
        return int(width)
    except (ValueError, TypeError):
        return 2


def keep_tuples(output):
    return [item for item in output if item.__class__ == tuple]


def shorten_output(output):
    if len(output) < 2:
        return output
    else:
        i = len(output)
        idx = int(math.log(i * 4) * math.log(i * 4))
        random.shuffle(output)
        return output[:idx]