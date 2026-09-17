from ast_nodes import (
    Program,
    Declaration,
    IfStatement,
    PrintStatement,
    BinaryExpression,
    Identifier,
    IntegerLiteral,
    StringLiteral,
)


def _describe(node):
    """Return a short one-line label for a single AST node."""

    if isinstance(node, Program):
        return "Program"

    if isinstance(node, Declaration):
        return f"Declaration (type={node.data_type}, name={node.name})"

    if isinstance(node, IfStatement):
        return "IfStatement"

    if isinstance(node, PrintStatement):
        return "Print"

    if isinstance(node, BinaryExpression):
        return f"BinaryExpression({node.operator})"

    if isinstance(node, Identifier):
        return f"Identifier({node.name})"

    if isinstance(node, IntegerLiteral):
        return f"IntegerLiteral({node.value})"

    if isinstance(node, StringLiteral):
        return f"StringLiteral({node.value!r})"

    return repr(node)


def _children(node):
    """
    Return this node's children as a list of (label, child) pairs.
    label is None when the child needs no name (e.g. left/right of a
    binary expression). A child may itself be a list of statements
    (e.g. an if-statement's then/else block) - the printer below
    knows how to expand that.
    """

    if isinstance(node, Program):
        return [(None, statement) for statement in node.statements]

    if isinstance(node, Declaration):
        return [("value", node.value)]

    if isinstance(node, IfStatement):
        children = [
            ("condition", node.condition),
            ("then", node.then_block),
        ]
        if node.else_block is not None:
            children.append(("else", node.else_block))
        return children

    if isinstance(node, PrintStatement):
        return [(None, argument) for argument in node.arguments]

    if isinstance(node, BinaryExpression):
        return [(None, node.left), (None, node.right)]

    # Identifier, IntegerLiteral, StringLiteral are leaves - no children
    return []


def _print_children(children, prefix):
    for index, (label, child) in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "

        if isinstance(child, list):
            # A block of statements (then/else) - print the label as a
            # bare grouping line, then descend into each statement.
            print(f"{prefix}{connector}{label}:")
            _print_children(
                [(None, item) for item in child],
                prefix + extension,
            )
        else:
            text = _describe(child)
            if label is not None:
                text = f"{label}: {text}"

            print(f"{prefix}{connector}{text}")
            _print_children(_children(child), prefix + extension)


def print_ast(root):
    """Pretty-print an AST rooted at `root` as an indented branch diagram."""

    print(_describe(root))
    _print_children(_children(root), prefix="")