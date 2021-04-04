import random
import ast
from string import ascii_lowercase, digits


def clean_name(name):
    name = "".join([c for c in name if c in ascii_lowercase])
    numbers = "".join([c for c in name if c in digits])
    return name, numbers


def combine_names(name1, name2, idx):
    name1, numbers1 = clean_name(name1)
    name2, numbers2 = clean_name(name2)
    if name1 == name2:
        name = name1
    else:
        name = "_".join(sorted([name1, name2]))
    if numbers1 == numbers2:
        numbers = numbers1
    else:
        numbers = "-".join(sorted([numbers1, numbers2]))
    return "_".join([name, numbers, str(idx)])


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