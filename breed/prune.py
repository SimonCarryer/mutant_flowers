import ast
import random


def prune(child):
    counter = PruneCounter()
    counter.visit(child)
    target = random.randint(0, counter.count)
    pruner = Pruner(target)
    pruner.visit(child)
    return child


target_fields = ["orelse", "body"]


class PruneCounter(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.target_fields = target_fields

    def generic_visit(self, node):
        for field, contents in ast.iter_fields(node):
            f = getattr(node, field)
            if field in self.target_fields and len(f) > 0:
                self.count += 1
        super().generic_visit(node)

    def visit_FunctionDef(self, node):
        if len(node.body) > 3:
            self.generic_visit(node)
        else:
            self.count = -1


class Pruner(ast.NodeTransformer):
    def __init__(self, target_count):
        super().__init__()
        self.target_count = target_count
        self.target_fields = target_fields
        self.count = 0

    def generic_visit(self, node):
        for field, contents in ast.iter_fields(node):
            f = getattr(node, field)
            if field in self.target_fields and len(f) > 0:
                self.count += 1
                if self.count == self.target_count:
                    if len(f) > 1:
                        remove = random.randint(0, len(f))
                        new = [node for idx, node in enumerate(f) if idx != remove]
                        setattr(node, field, new)
                        # print(
                        #     f"set contents of {node.__class__} {field} to len {len(new)}"
                        # )
                    else:
                        # print(f"removing whole of {node.__class__}")
                        return None
        super().generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        for field, contents in ast.iter_fields(node):
            f = getattr(node, field)
            if field in self.target_fields and len(f) > 0:
                self.count += 1
                if self.count == self.target_count:
                    if len(f) > 3:
                        remove = random.randint(1, len(f) - 1)
                        new = [
                            node
                            for idx, node in enumerate(f)
                            if idx != remove or node.__class__ == ast.Return
                        ]
                        # print(
                        #     f"set contents of {node.__class__} {field} to len {len(new)}"
                        # )
                        setattr(node, field, new)
        super().generic_visit(node)
        return node