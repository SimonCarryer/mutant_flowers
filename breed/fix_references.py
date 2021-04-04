import ast
import random
from copy import copy


def fix_references(child):
    fixer = ReferenceFixer()
    fixer.visit(child, [])
    return child


class ReferenceFixer(ast.NodeTransformer):
    def visit_FunctionDef(self, node, assigned_names):
        assigned_names = copy(assigned_names)
        args = node.args
        for arg in args.posonlyargs + args.args + args.kwonlyargs:
            assigned_names.append(arg.arg)
        self.generic_visit(node, assigned_names)
        return node

    def visit(self, node, assigned_names):
        if node.__class__ == ast.FunctionDef:
            self.visit_FunctionDef(node, assigned_names)
        elif node.__class__ == ast.Name:
            self.visit_Name(node, assigned_names)
        elif node.__class__ == ast.Call:
            self.visit_Call(node, assigned_names)
        elif node.__class__ == ast.For:
            self.visit_For(node, assigned_names)
        else:
            self.generic_visit(node, assigned_names)
        return node

    def visit_For(self, node, assigned_names):
        if isinstance(node.target, ast.AST):
            self.generic_visit(node, assigned_names)
        else:
            for n in node.target:
                self.generic_visit(n, assigned_names)

    def generic_visit(self, node, assigned_names):
        for field, old_value in ast.iter_fields(node):
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, ast.AST):
                        value = self.visit(value, assigned_names)
                        if value is None:
                            continue
                        elif not isinstance(value, ast.AST):
                            new_values.extend(value)
                            continue
                    new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, ast.AST):
                new_node = self.visit(old_value, assigned_names)
                if new_node is None:
                    delattr(node, field)
                else:
                    setattr(node, field, new_node)
        return node

    def visit_Name(self, node, assigned_names):
        if node.ctx.__class__ == ast.Store:
            assigned_names.append(node.id)
        elif node.ctx.__class__ == ast.Load and node.id not in assigned_names:
            node.id = random.choice(assigned_names)
        self.generic_visit(node, assigned_names)
        return node

    def visit_Call(self, node, assigned_names):
        if hasattr(node.func, "id") and node.func.id:
            assigned_names.append(node.func.id)
        self.generic_visit(node, assigned_names)
        return node