import random
import ast
from string import ascii_lowercase

names = ["gen", "forward", "turn", "width", "colour"]
defaults = [40, 1, 3, 1]

comparators = [
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
]

operators = [ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod]


def random_function(name):
    args = build_args(names, defaults)
    body = [build_assign_node(), expression(), build_return_node()]
    function = ast.FunctionDef(name=name, args=args, body=body, decorator_list=[])
    ast.fix_missing_locations(function)
    return function


def build_assign_node():
    assign_node = ast.Assign(
        targets=[ast.Name(id="output", ctx=ast.Store())],
        value=ast.List(elts=[], ctx=ast.Load()),
    )
    ast.fix_missing_locations(assign_node)
    return assign_node


def build_return_node():
    return ast.Return(value=ast.Name(id="output", ctx=ast.Load()))


def build_args(names, defaults):
    args = [ast.arg(arg=name) for name in names]
    defaults = [ast.Constant(value=value) for value in defaults]
    return ast.arguments(
        posonlyargs=[], args=args, kwonlyargs=[], kw_defaults=[], defaults=defaults
    )


def binop(id=None, extra_vars=None):
    if id is None:
        left = var(extra_vars=extra_vars)
    else:
        left = ast.Name(id=id, ctx=ast.Load())
    right = var_or_constant(extra_vars=extra_vars)
    op = random.choice(operators)()
    return ast.BinOp(left=left, right=right, op=op)


def var_or_binop(id=None, extra_vars=None):
    if id is None:
        value = var(extra_vars=extra_vars)
    else:
        value = ast.Name(id=id, ctx=ast.Load())
    return random.choice([value, binop(id=id)])


def append_tuple_to_output(extra_vars=None):
    value = ast.Name("output", ctx=ast.Load())
    attr = "append"
    func = ast.Attribute(value=value, attr=attr, ctx=ast.Load())
    elts = [binop(name, extra_vars=extra_vars) for name in names[1:]]
    args = [ast.Tuple(elts=elts, ctx=ast.Load())]
    call = ast.Call(func=func, args=args, keywords=[])
    return ast.Expr(value=call)


def aug_assign(extra_vars=None):
    target = var(extra_vars=extra_vars)
    target.ctx = ast.Store()
    op = random.choice(operators)()
    value = var_or_constant(extra_vars=None)
    return ast.AugAssign(target=target, op=op, value=value)


def expression(extra_vars=None):
    value = random.choice(
        [
            append_tuple_to_output,
            aug_assign,
            build_if,
            build_for,
        ]
    )
    return value(extra_vars=extra_vars)


def var(extra_vars=None):
    if extra_vars is None:
        extra_vars = []
    name = random.choice(names + extra_vars + extra_vars)
    return ast.Name(name, ctx=ast.Load())


def constant(extra_vars=None):
    value = random.randint(1, 10)
    return ast.Constant(value)


def var_or_constant(extra_vars=None):
    return random.choice([var, constant])(extra_vars=extra_vars)


def compare(extra_vars=None):
    left = var(extra_vars=extra_vars)
    right = constant()
    comparitor = random.choice(comparators)()
    return ast.Compare(left=left, comparators=[right], ops=[comparitor])


def build_if(extra_vars=None):
    test = compare(extra_vars=extra_vars)
    body = [expression(extra_vars=extra_vars)]
    return ast.If(test=test, body=body, orelse=[])


def build_for(extra_vars=None):
    var_name = random.choice(ascii_lowercase)
    target = ast.Name(id=var_name, ctx=ast.Store())
    func = ast.Name(id="range", ctx=ast.Load())
    args = [var_or_constant(extra_vars=extra_vars)]
    iter_ = ast.Call(target=target, func=func, args=args, keywords=[])
    body = [expression(extra_vars=[var_name])]
    return ast.fix_missing_locations(
        ast.For(target=target, iter=iter_, body=body, orelse=[])
    )
