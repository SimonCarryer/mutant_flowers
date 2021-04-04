import ast
import random


def prune(child):
    counter = PruneCounter()
    counter.visit(child)
    target = random.randint(0, counter.count)
    mutator = Pruner(target)
    mutator.visit(child)
    return child


class PruneCounter(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.count = 0

    def generic_visit(self, node):
        if hasattr(node, "body") and node.body.__class__ == list and len(node.body) > 1:
            self.count += 1
        super().generic_visit(node)


class Pruner(ast.NodeTransformer):
    def __init__(self, target_count):
        super().__init__()
        self.target_count = target_count
        self.count = 0

    def generic_visit(self, node):
        if hasattr(node, "body") and node.body.__class__ == list and len(node.body) > 1:
            self.count += 1
            if self.count == self.target_count:
                remove = random.randint(0, len(node.body))
                node.body = [
                    node for idx, node in enumerate(node.body) if idx != remove
                ]
        super().generic_visit(node)
        return node