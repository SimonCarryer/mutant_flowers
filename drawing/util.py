import turtle


def write_function_name(name):
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    t.goto(-320, 250)
    t.write(name, font=("Arial", 24, "normal"))