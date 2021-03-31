import ast
import inspect
from breed.crossover import crossover
from breed.inject import inject
from breed.rename import rename_function, NameGetter


def function_to_ast(function):
    return ast.parse(inspect.getsource(function)).body[0]


def ast_to_function(function_ast):
    namespace = {}
    n = NameGetter()
    n.visit(function_ast)
    basket = ast.Module([function_ast], [])
    exec(compile(basket, filename="<ast>", mode="exec"), namespace)
    return namespace[n.name]


def make_baby(parent_1, parent_2, name_idx=0):
    parent_1 = function_to_ast(parent_1)
    parent_2 = function_to_ast(parent_2)
    original = ast.dump(parent_2)
    inject(parent_1, parent_2)
    crossover(parent_1, parent_2)
    new_ast = rename_function(parent_1, parent_2, parent_2, name_idx)
    return ast_to_function(new_ast)


def make_babies(parent_1, parent_2, n_babies=10):
    babies = 0
    while babies < n_babies:
        try:
            func = make_baby(parent_1, parent_2, name_idx=babies)
            if all([func(i).__class__ == list for i in range(10)]):
                babies += 1
                yield func
        except:
            pass