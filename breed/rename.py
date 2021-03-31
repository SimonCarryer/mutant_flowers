import random
import ast
from string import ascii_lowercase


def clean_name(name):
    return "".join([c for c in name if c in ascii_lowercase])


def combine_names(name1, name2, idx):
    return "_".join([clean_name(name1), clean_name(name2), str(idx)])


def rename_function(parent_1, parent_2, new_function, idx):
    n1 = NameGetter()
    n1.visit(parent_1)
    name1 = n1.name
    n2 = NameGetter()
    n2.visit(parent_2)
    name2 = n2.name
    name = combine_names(name1, name2, idx)
    renamer = Renamer(name)
    renamer.visit(new_function)
    return new_function


class NameGetter(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        self.name = node.name
        super().generic_visit(node)


class Renamer(ast.NodeTransformer):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def visit_FunctionDef(self, node):
        node.name = self.name
        super().generic_visit(node)