import turtle
import random


def copy_turtle(t):
    t = t.clone()
    t.hideturtle()
    return t


def init_turtle():
    t = turtle.Turtle()
    t.left(90)
    turtle.colormode(255)
    t.pencolor((40, 20, 0))
    t.width(5)
    t.hideturtle()
    return t


pallette = {0: "#507667", 1: "#ffd0ca", 2: "#fe9578", 3: "#eacf0e", 4: "#ada990"}


def lookup_colour(colour):
    return pallette[colour % (len(pallette) - 1)]


def interpret_output(t, forward, turn, width, colour):
    try:
        width_ = t.width()
        t.width(min(max(width_ + width, 0), 8))
        t.pencolor(lookup_colour(colour))
        t.left(turn)
        t.forward(forward)
        return t
    except:
        return None


def prune_turtles(turtles):
    random.shuffle(turtles)
    return turtles[:36]
