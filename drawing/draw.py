import turtle
import random
import time
from .util import *
from .regulate import regulate


def interpret_output(t, forward, turn, width, colour, highlight=True):
    try:
        width_ = t.width()
        t.width(min(max(width, 3), 18))
        c = lookup_colour(int(colour))
        t2 = copy_turtle(t)
        t2.setx(t.xcor() + 3)
        t.pencolor(darken(c))
        t.pendown()
        t.left(turn)
        t.forward(forward)
        t.penup()
        t2.pendown()
        t2.pencolor(c)
        t2.left(turn)
        t2.forward(forward)
        t2.penup()
    except TypeError:
        return None
    return t


def draw_from_function(func, start=(0, 0), incremental=True):
    turtle.hideturtle()
    t = init_turtle(start)
    write_function_name(func.__name__, start)
    turtles = [t]
    gen = 0
    while len(turtles) > 0:
        new_turtles = []
        for t in turtles:
            if gen < 10 and t is not None:
                output = regulate(func(gen))
                for forward, turn, width, rgb in output:
                    new_turtles += [
                        interpret_output(copy_turtle(t), forward, turn, width, rgb)
                    ]
        turtles = prune_turtles(new_turtles)
        if incremental:
            turtle.update()
        gen += 1
    if not incremental:
        turtle.getscreen().update()
        time.sleep(1)


def draw_highlight(t, forward, turn, width, colour):
    try:
        width_ = t.width() - 3
        if width_ > 0:
            t.sety(t.ycor() - 0.2)
            t.width(min(max(width_ + width, 1), 12))
            c = lighten(lookup_colour(colour))
            t.pencolor(c)
            t.left(turn)
            t.forward(forward + 0.2)
    except:
        pass
