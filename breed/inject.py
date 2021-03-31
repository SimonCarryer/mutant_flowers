from collections import defaultdict
import random
import ast

classes = [
    ast.Name,
    ast.If,
    ast.Compare,
    ast.Constant,
    ast.Expr,
    ast.BinOp,
    ast.Add,
    ast.Mult,
    ast.Eq,
    ast.And,
    ast.Or,
    ast.Sub,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
    ast.Call,
    ast.For,
]


def inject(parent_1, parent_2):
    collector = InjectCollector()
    collector.visit(parent_1)
    counter = InjectCounter(collector.collected_nodes)
    counter.visit(parent_2)
    target = random.randint(0, counter.count)
    injector = Injector(collector.collected_nodes, target)
    injector.visit(parent_2)
    ast.fix_missing_locations(parent_2)
    return parent_2


class InjectCollector(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.collected_nodes = []
        self.classes = classes

    def generic_visit(self, node):
        if hasattr(node, "body") and node.body.__class__ == list:
            self.collected_nodes += [
                n for n in node.body if n.__class__ in self.classes
            ]
        super().generic_visit(node)


class InjectCounter(ast.NodeVisitor):
    def __init__(self, collected_nodes):
        super().__init__()
        self.count = 0

    def generic_visit(self, node):
        if hasattr(node, "body") and node.body.__class__ == list:
            self.count += 1
        super().generic_visit(node)


class Injector(ast.NodeTransformer):
    def __init__(self, collected_nodes, target_count):
        super().__init__()
        self.collected_nodes = collected_nodes
        self.target_count = target_count
        self.count = 0

    def generic_visit(self, node):
        if hasattr(node, "body") and node.body.__class__ == list:
            self.count += 1
            if self.count == self.target_count:
                new_node = random.choice(self.collected_nodes)
                node.body = node.body[:-1] + [new_node] + [node.body[-1]]
                return node
        super().generic_visit(node)
        return node