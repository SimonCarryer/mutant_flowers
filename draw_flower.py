import time
import turtle
from drawing.draw import draw_from_function
from drawing.util import (
    write_function_name,
    clear_screen,
    fill_background,
    set_up_screen,
)
from breed.babies import BabyMaker
from plants.plants import tree, daisy, cyclamen, foxglove, generated_flower


def draw_functions(maker, f1, f2):
    xs = range(80, 800, 200)
    ys = range(600, 0, -250)
    coords = [(x, y) for y in ys for x in xs]
    funcs = list(maker.make_babies(f1, f2))
    for func, start in zip([f1, f2], coords):
        draw_from_function(func, start=start, incremental=True)
    for func, start in zip(funcs, coords[2:]):
        draw_from_function(func, start=start, incremental=True)
    return funcs


if __name__ == "__main__":
    f1 = generated_flower
    set_up_screen()
    draw_from_function(f1, start=(400, 0), incremental=True)
    while True:
        pass
