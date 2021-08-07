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
from breed.breeder import Breeder
from plants.plants import tree, daisy, cyclamen, foxglove


def flower_like(outputs):
    stem_length = 4
    sizes = [len(o) for o in outputs]
    # forwards = [max([o[0] for o in output]) if len(output) > 0 else 0 for output in outputs]
    turns = [
        max([o[1] for o in output]) if len(output) > 0 else 0 for output in outputs
    ]
    width = [
        max([o[2] for o in output]) if len(output) > 0 else 0 for output in outputs
    ]
    # colours = [set([o[3] for o in output])  if len(output) > 0 else set() for output in outputs]
    if any([s == 0 for s in sizes[:stem_length]]):
        factor = 0.1
    else:
        factor = 1
    size_of_stem = 0
    size_of_flower = 0
    shape_of_flower = 0
    if len(sizes) > 0:
        size_of_stem = sum(sizes[:stem_length])
        size_of_flower = sum(sizes[stem_length:]) / 3
        shape_of_flower = len(set(turns[stem_length:])) * 1.5
    score = (size_of_flower + shape_of_flower) - size_of_stem
    return max([score * factor, 0.1])


fitness = flower_like


def draw_functions(functions):
    xs = range(80, 800, 200)
    ys = range(600, 0, -250)
    coords = [(x, y) for y in ys for x in xs]
    for func, start in zip(functions, coords):
        draw_from_function(func, start=start, incremental=True)


if __name__ == "__main__":
    maker = BabyMaker(inject=1, crossover=1, mutate=1, prune=0.4)
    breeder = Breeder(
        maker,
        fitness,
        n_generations=11,
        starting_functions=400,
        generation_size=40,
        tournament_size=8,
        stopping_fitness=25,
    )
    breeder.breed()
    functions = breeder.runs[-1].hall_of_fame
    set_up_screen()
    print(f"drawing {len(functions)} functions")
    draw_functions(functions)
    for func in breeder.hall_of_fame():
        print(func, end="\n\n")
    while True:
        pass
