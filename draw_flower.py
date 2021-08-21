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
from plants.plants import (
    tree,
    daisy,
    cyclamen,
    foxglove,
    generated_flower,
    good_flower,
    func__14_23,
)


if __name__ == "__main__":
    f1 = func__14_23
    set_up_screen()
    draw_from_function(f1, start=(400, 400), incremental=True)
    while True:
        pass
