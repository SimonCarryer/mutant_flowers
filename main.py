import time
from drawing.draw import *
from drawing.util import write_function_name
from breed.babies import make_babies
from plants.plants import tree, flower


def draw_from_function(func):
    turtle.getscreen().clear()
    turtle.getscreen().bgcolor("#ada990")
    turtle.hideturtle()
    turtle.update()
    write_function_name(func.__name__)
    turtle.tracer(0, 0)
    t = init_turtle()
    turtles = [t]
    gen = 0
    while len(turtles) > 0:
        new_turtles = []
        for t in turtles:
            if gen < 10 and t is not None:
                output = func(gen)
                new_turtles += [
                    interpret_output(copy_turtle(t), forward, turn, width, rgb)
                    for forward, turn, width, rgb in output
                ]
        turtles = prune_turtles(new_turtles)
        turtle.update()
        gen += 1
        time.sleep(0.25)


if __name__ == "__main__":
    for func in [tree, flower]:
        draw_from_function(func)
    for func in make_babies(tree, flower):
        draw_from_function(func)
