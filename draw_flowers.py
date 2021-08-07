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


def draw_functions(functions):
    xs = range(80, 800, 200)
    ys = range(600, 0, -250)
    coords = [(x, y) for y in ys for x in xs]
    for func, start in zip(functions, coords):
        draw_from_function(func, start=start, incremental=True)


if __name__ == "__main__":
    set_up_screen()
    functions = [daisy, cyclamen, foxglove, tree]
    time.sleep(6)
    draw_functions(functions)
