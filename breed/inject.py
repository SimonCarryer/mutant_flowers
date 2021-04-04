from collections import defaultdict
import random
import ast

target_fields = ["orelse", "body"]


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
        self.collected_nodes = defaultdict(list)
        self.target_fields = target_fields

    def generic_visit(self, node):
        for field, contents in ast.iter_fields(node):
            f = getattr(node, field)
            if field in self.target_fields and len(f) > 0:
                self.collected_nodes[field] += f
        super().generic_visit(node)

    def visit_FunctionDef(self, node):
        if len(node.body) > 2:
            self.collected_nodes["body"] += node.body[1:-1]
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
                    new_node = random.choice(self.collected_nodes[field])
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
                    new_node = random.choice(self.collected_nodes[field])
                    contents = getattr(node, field)
                    idx = random.randint(1, len(contents) - 1)
                    new_contents = contents[:idx] + [new_node] + contents[idx:]
                    setattr(node, field, new_contents)
        super().generic_visit(node)
        return node