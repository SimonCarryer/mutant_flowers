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
from breed.fitness_functions import flower_like, naive, daisy_like, daisy_like_1

fitness = daisy_like_1


def draw_functions(functions):
    xs = range(80, 800, 200)
    ys = range(600, 0, -250)
    coords = [(x, y) for y in ys for x in xs]
    for func, start in zip(functions, coords):
        draw_from_function(func, start=start, incremental=True)


if __name__ == "__main__":
    maker = BabyMaker(inject=1, crossover=1, mutate=1, prune=0.9)
    breeder = Breeder(
        maker,
        fitness,
        n_generations=11,
        starting_functions=800,
        generation_size=70,
        tournament_size=3,
        stopping_fitness=25,
    )
    breeder.breed()
    functions = breeder.runs[-1].hall_of_fame
    set_up_screen()
    print(f"drawing {len(functions)} functions")
    draw_functions(functions)
    for func in breeder.hall_of_fame()[-11:]:
        print(func, end="\n\n")
    while True:
        pass
