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


def crossover(subject, donor):
    collector = CrossoverCollector()
    collector.visit(donor)
    counter = CrossoverCounter(collector.collected_nodes)
    counter.visit(subject)
    target = random.randint(0, counter.count)
    pollinator = CrossPollinator(collector.collected_nodes, target)
    pollinator.visit(subject)
    return subject


class CrossoverCollector(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.collected_nodes = []
        self.classes = classes

    def generic_visit(self, node):
        if node.__class__ in self.classes:
            self.collected_nodes.append(node)
        super().generic_visit(node)


class CrossoverCounter(ast.NodeVisitor):
    def __init__(self, collected_nodes):
        super().__init__()
        self.classes = [node.__class__ for node in collected_nodes]
        self.count = 0

    def generic_visit(self, node):
        if node.__class__ in self.classes:
            self.count += 1
        super().generic_visit(node)


class CrossPollinator(ast.NodeTransformer):
    def __init__(self, collected_nodes, target_count):
        super().__init__()
        self.collected_nodes = collected_nodes
        self.classes = [node.__class__ for node in collected_nodes]
        self.target_count = target_count
        self.count = 0

    def generic_visit(self, node):
        if node.__class__ in self.classes and node.__class__ != ast.Name:
            self.count += 1
            if self.count == self.target_count:
                new_node = random.choice(
                    [
                        new
                        for new in self.collected_nodes
                        if new.__class__ == node.__class__
                    ]
                )
                if hasattr(new_node, "ctx"):
                    new_node.ctx = node.ctx
                return new_node
        super().generic_visit(node)
        return node
