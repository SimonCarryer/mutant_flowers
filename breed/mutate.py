import ast
import random

classes = [ast.Constant, ast.BinOp, ast.Compare, ast.Name]
operators = [ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod]
comparitors = [
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
]


def mutate(child):
    counter = MutateCounter()
    counter.visit(child)
    target = random.randint(0, counter.count)
    mutator = Mutator(target, counter.names)
    mutator.visit(child)
    ast.fix_missing_locations(child)
    return child


class MutateCounter(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.classes = classes
        self.names = []
        self.count = 0

    def visit_Name(self, node):
        self.names.append(node.id)
        self.generic_visit(node)

    def generic_visit(self, node):
        if node.__class__ in self.classes:
            self.count += 1
        super().generic_visit(node)


class Mutator(ast.NodeTransformer):
    def __init__(self, target_count, names):
        super().__init__()
        self.names = names
        self.classes = classes
        self.target_count = target_count
        self.count = 0

    def generic_visit(self, node):
        if node.__class__ in self.classes:
            self.count += 1
        super().generic_visit(node)
        return node

    def visit_BinOp(self, node):
        if self.count == self.target_count:
            old_operator = node.op
            new_operator = random.choice(
                [op for op in operators if op != old_operator.__class__]
            )
            node.op = new_operator()
        self.generic_visit(node)
        return node

    def visit_Constant(self, node):
        if self.count == self.target_count:
            value = node.value
            if value.__class__ == int:
                roll = random.randint(0, 3)
                if roll == 0:
                    node.value = value + 1
                elif roll == 1:
                    node.value = value - 1
                elif roll == 2:
                    node.value = -value
                else:
                    node = ast.Name(id=random.choice(self.names), ctx=ast.Load())
        self.generic_visit(node)
        return node

    def visit_Compare(self, node):
        if self.count == self.target_count:
            old_ops = node.ops
            new_ops = []
            for old_op in old_ops:
                new_op = random.choice(
                    [op for op in comparitors if op != old_op.__class__]
                )
                new_ops.append(new_op())
            node.ops = new_ops
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if self.count == self.target_count:
            node.id = random.choice([name for name in self.names if name != node.id])
            self.count += 1
        super().generic_visit(node)
        return node