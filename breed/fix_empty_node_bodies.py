import ast


def fix_empty_node_bodies(child):
    fixer = EmptyNodeFixer()
    fixer.visit(child)
    return child


class EmptyNodeFixer(ast.NodeTransformer):
    def generic_visit(self, node):
        if hasattr(node, "body") and node.body == []:
            # print("found an empty!")
            if node.__class__ == ast.If:
                if node.orelse != []:
                    node.body = node.orelse
                    node.orelse = []
                else:
                    return None
        super().generic_visit(node)
        return node