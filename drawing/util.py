import turtle
import random

pallette = {0: "#ada990", 1: "#ffd0ca", 2: "#fe9578", 3: "#eacf0e", 4: "#507667"}


def copy_turtle(t):
    t = t.clone()
    t.hideturtle()
    return t


def init_turtle(start):
    t = turtle.Turtle()
    t.penup()
    t.setpos(start)
    t.pendown()
    t.left(90)
    t.width(5)
    t.hideturtle()
    return t


def prune_turtles(turtles):
    random.shuffle(turtles)
    return turtles[:36]


def lookup_colour(colour):
    value = pallette[colour % (len(pallette) - 1)]
    return hex_to_rgb(value)


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def lighten(rgb):
    return (min([c + 40, 255]) for c in rgb)


def darken(rgb):
    return (max([c - 40, 0]) for c in rgb)


def write_function_name(name, position):
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.goto(position[0], position[1] - 45)
    t.write(name, font=("Consolas", 16, "normal"), align="center")


def clear_screen():
    turtle.getscreen().clear()
    turtle.hideturtle()


def fill_background():
    turtle.getscreen().bgcolor(hex_to_rgb(pallette[len(pallette) - 1]))


def set_up_screen():
    turtle.getscreen().setup(width=800, height=800, startx=0, starty=0)
    turtle.setworldcoordinates(0, 0, 800, 800)
    turtle.getscreen().tracer(0, 0)
    turtle.getscreen().colormode(255)