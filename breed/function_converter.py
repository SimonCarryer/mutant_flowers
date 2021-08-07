import ast
from breed.rename import rename_function, NameGetter
import inspect


class FunctionConverter:
    def __init__(self):
        self.namespace = {}
        self.stored_asts = {}

    def function_to_ast(self, function):
        try:
            function_ast = self.stored_asts[function.__name__]
        except KeyError:
            source = inspect.getsource(function)
            function_ast = ast.parse(source).body[0]
            self.stored_asts[function.__name__] = function_ast
        return function_ast

    def ast_to_function(self, function_ast):
        n = NameGetter()
        n.visit(function_ast)
        basket = ast.Module([function_ast], [])
        exec(compile(basket, filename="<ast>", mode="exec"), self.namespace)
        self.stored_asts[n.name] = function_ast
        return self.namespace[n.name]

    def source_for_function(self, function):
        function_ast = self.stored_asts[function.__name__]
        return ast.unparse(function_ast)
