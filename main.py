import time
import turtle
from drawing.draw import draw_from_function
from drawing.util import (
    write_function_name,
    clear_screen,
    fill_background,
    set_up_screen,
)
from breed.babies import make_babies
from plants.plants import tree, flower


if __name__ == "__main__":
    set_up_screen()
    # fill_background()
    xs = range(80, 800, 200)
    ys = range(600, 0, -250)
    coords = [(x, y) for y in ys for x in xs]
    for func, start in zip([tree, flower], coords):
        # clear_screen()
        # fill_background()
        draw_from_function(func, start=start, incremental=True)
    for func, start in zip(make_babies(tree, flower), coords[2:]):
        # clear_screen()
        # fill_background()
        draw_from_function(func, start=start, incremental=True)
    turtle.getscreen().getcanvas().postscript(file="images/flowers.eps")
