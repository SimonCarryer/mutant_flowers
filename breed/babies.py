import ast
import inspect
import random
from breed.crossover import crossover
from breed.inject import inject
from breed.rename import rename_function, NameGetter
from breed.mutate import mutate
from breed.prune import prune
from breed.fix_references import fix_references
from breed.fix_empty_node_bodies import fix_empty_node_bodies


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

    def make_baby(self, parent_1, parent_2, name_idx=0):
        parent_1 = self.function_converter.function_to_ast(parent_1)
        parent_2 = self.function_converter.function_to_ast(parent_2)
        parent_1, parent_2 = random.sample([parent_1, parent_2], 2)
        if self.inject:
            inject(parent_1, parent_2)
        if self.crossover:
            crossover(parent_1, parent_2)
        new_ast = rename_function(parent_1, parent_2, parent_2, name_idx)
        if self.prune:
            prune(new_ast)
        if self.mutate:
            mutate(new_ast)
        fix_references(new_ast)
        fix_empty_node_bodies(new_ast)
        return self.function_converter.ast_to_function(new_ast)

    def make_babies(self, parent_1, parent_2, n_babies=10):
        babies = 0
        failures = 0
        while babies < n_babies and failures < (n_babies * 10):
            try:
                func = self.make_baby(parent_1, parent_2, name_idx=babies)
                if all([func(i).__class__ == list for i in range(10)]):
                    babies += 1
                    yield func
            except:
                failures += 1