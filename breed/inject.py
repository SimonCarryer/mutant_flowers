from collections import defaultdict
import random
import ast

target_fields = ["orelse", "body"]


def inject(subject, donor):
    collector = InjectCollector()
    collector.visit(donor)
    counter = InjectCounter(collector.collected_nodes)
    counter.visit(subject)
    target = random.randint(0, counter.count)
    injector = Injector(collector.collected_nodes, target)
    injector.visit(subject)
    return subject


class InjectCollector(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.collected_nodes = []
        self.target_fields = target_fields

    def generic_visit(self, node):
        for field, contents in ast.iter_fields(node):
            f = getattr(node, field)
            if field in self.target_fields and len(f) > 0:
                self.collected_nodes += f
        super().generic_visit(node)

    def visit_FunctionDef(self, node):
        if len(node.body) > 2:
            self.collected_nodes += node.body[1:-1]
        super().generic_visit(node)


class InjectCounter(ast.NodeVisitor):
    def __init__(self, collected_nodes):
        super().__init__()
        self.count = 0
        self.target_fields = target_fields

    def generic_visit(self, node):
        for field, contents in ast.iter_fields(node):
            f = getattr(node, field)
            if field in self.target_fields and len(f) > 0:
                self.count += 1
        super().generic_visit(node)


class Injector(ast.NodeTransformer):
    def __init__(self, collected_nodes, target_count):
        super().__init__()
        self.collected_nodes = collected_nodes
        self.target_count = target_count
        self.target_fields = target_fields
        self.count = 0

    def generic_visit(self, node):
        for field, contents in ast.iter_fields(node):
            f = getattr(node, field)
            if field in self.target_fields and len(f) > 0:
                self.count += 1
                if self.count == self.target_count:
                    new_node = random.choice(self.collected_nodes)
                    contents = getattr(node, field)
                    idx = random.randint(0, len(contents))
                    new_contents = contents[:idx] + [new_node] + contents[idx:]
                    setattr(node, field, new_contents)
        super().generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        for field, contents in ast.iter_fields(node):
            f = getattr(node, field)
            if field in self.target_fields and len(f) > 0:
                self.count += 1
                if self.count == self.target_count:
                    new_node = random.choice(self.collected_nodes)
                    contents = getattr(node, field)
                    idx = random.randint(1, len(contents) - 1)
                    new_contents = contents[:idx] + [new_node] + contents[idx:]
                    setattr(node, field, new_contents)
        super().generic_visit(node)
        return node