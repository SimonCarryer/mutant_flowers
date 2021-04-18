import ast
import inspect
import random
from breed.crossover import crossover
from breed.inject import inject
from breed.rename import rename_function, NameGetter
from breed.mutate import mutate, fix_functiondef
from breed.prune import prune
from breed.fix_references import fix_references
from breed.fix_empty_node_bodies import fix_empty_node_bodies
from breed.random_function import random_function
from copy import deepcopy
from time import perf_counter


class FunctionConverter:
    def __init__(self):
        self.namespace = {}
        self.function_source = {}

    def function_to_ast(self, function):
        source = self.source_for_function(function)
        return ast.parse(source).body[0]

    def ast_to_function(self, function_ast):
        n = NameGetter()
        n.visit(function_ast)
        basket = ast.Module([function_ast], [])
        exec(compile(basket, filename="<ast>", mode="exec"), self.namespace)
        source = ast.unparse(basket)
        self.function_source[n.name] = source
        return self.namespace[n.name]

    def source_for_function(self, function):
        try:
            source = inspect.getsource(function)
        except OSError:
            source = self.function_source[function.__name__]
        return source


class BabyMaker:
    def __init__(self, inject=True, crossover=True, mutate=True, prune=True):
        self.inject = inject
        self.crossover = crossover
        self.mutate = mutate
        self.prune = prune
        self.function_converter = FunctionConverter()
        self.max_nodes = 800

    def clear_functions(self):
        self.function_converter = FunctionConverter()

    def generate_functions(self, n_functions):
        i = 0
        failures = 0
        while i < n_functions and failures < n_functions * 5:
            generated_ast = random_function(f"func_{i}")
            func = self.function_converter.ast_to_function(generated_ast)
            try:
                func(0)
                yield func
                i += 1
            except:
                failures += 1

    def baby(self, parent_1, parent_2, name_idx=0):
        new_ast, other_ast = random.sample([parent_1, parent_2], 2)
        if self.inject > random.random():
            new_ast = inject(deepcopy(new_ast), deepcopy(other_ast))
        if self.crossover > random.random():
            new_ast = crossover(deepcopy(new_ast), deepcopy(other_ast))
        new_ast = rename_function(
            deepcopy(parent_1), deepcopy(parent_2), new_ast, name_idx
        )
        if self.prune > random.random():
            new_ast = prune(deepcopy(new_ast))
        if self.mutate > random.random():
            correct_args = [arg.arg for arg in new_ast.args.args]
            defaults = new_ast.args.defaults
            new_ast = mutate(deepcopy(new_ast))
            new_ast = fix_functiondef(new_ast, correct_args, defaults)
        new_ast = fix_references(new_ast)
        new_ast = fix_empty_node_bodies(new_ast)
        new_ast = ast.fix_missing_locations(new_ast)
        return new_ast

    def make_baby(self, parent_1, parent_2, name_idx=0):
        parent_1 = self.function_converter.function_to_ast(parent_1)
        parent_2 = self.function_converter.function_to_ast(parent_2)
        start = perf_counter()
        baby = None
        failures = 0
        while baby is None and failures < 100:
            func = self.baby(deepcopy(parent_1), deepcopy(parent_2), name_idx=name_idx)
            try:
                ast_length = len(list(ast.walk(func)))
                func = self.function_converter.ast_to_function(func)
                if all([func(i).__class__ == list for i in range(10)]):
                    baby = func
            except:
                failures += 1
        end = perf_counter()
        stats = {"time": end - start, "failures": failures, "size": ast_length}
        return baby, stats

    def make_babies(self, parent_1, parent_2, n_babies=10):
        parent_1 = deepcopy(self.function_converter.function_to_ast(parent_1))
        parent_2 = deepcopy(self.function_converter.function_to_ast(parent_2))
        babies = 0
        failures = 0
        while babies < n_babies and failures < (n_babies * 10):
            func = self.baby(deepcopy(parent_1), deepcopy(parent_2), name_idx=babies)
            try:
                func = self.function_converter.ast_to_function(func)
                if all([func(i).__class__ == list for i in range(10)]):
                    babies += 1
                    yield func
            except:
                failures += 1