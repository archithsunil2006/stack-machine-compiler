from ast_nodes import (
    Program,
    Declaration,
    Assignment,
    IfStatement,
    LoopStatement,
    PrintStatement,
    BinaryExpression,
    Identifier,
    IntegerLiteral,
    BooleanLiteral,
    CharacterLiteral,
    StringLiteral,
)


def print_ast(node):
    visit(node)


def visit(node, prefix="", is_last=True):
    connector = "└── " if is_last else "├── "

    if isinstance(node, Program):
        print("Program")

        for i, statement in enumerate(node.statements):
            visit(
                statement,
                "",
                i == len(node.statements) - 1
            )

    elif isinstance(node, Declaration):
        print(
            prefix
            + connector
            + f"Declaration (type={node.data_type}, "
              f"name={node.name})"
        )

        visit(
            node.value,
            prefix + ("    " if is_last else "│   "),
            True
        )

    elif isinstance(node, Assignment):
        print(
            prefix
            + connector
            + f"Assignment (name={node.name})"
        )

        visit(
            node.value,
            prefix + ("    " if is_last else "│   "),
            True
        )

    elif isinstance(node, IfStatement):
        print(prefix + connector + "If")

        child_prefix = prefix + (
            "    " if is_last else "│   "
        )

        visit(node.condition, child_prefix, False)

        for i, statement in enumerate(node.then_block):
            visit(
                statement,
                child_prefix,
                node.else_block is None
                and i == len(node.then_block) - 1
            )

        if node.else_block is not None:
            print(child_prefix + "└── Else")

            else_prefix = child_prefix + "    "

            for i, statement in enumerate(node.else_block):
                visit(
                    statement,
                    else_prefix,
                    i == len(node.else_block) - 1
                )

    elif isinstance(node, LoopStatement):
        print(prefix + connector + "Loop")

        child_prefix = prefix + (
            "    " if is_last else "│   "
        )

        visit(node.condition, child_prefix, False)

        for i, statement in enumerate(node.body):
            visit(
                statement,
                child_prefix,
                i == len(node.body) - 1
            )

    elif isinstance(node, PrintStatement):
        print(prefix + connector + "Print")

        child_prefix = prefix + (
            "    " if is_last else "│   "
        )

        for i, argument in enumerate(node.arguments):
            visit(
                argument,
                child_prefix,
                i == len(node.arguments) - 1
            )

    elif isinstance(node, BinaryExpression):
        print(
            prefix
            + connector
            + f"BinaryExpression('{node.operator}')"
        )

        child_prefix = prefix + (
            "    " if is_last else "│   "
        )

        visit(node.left, child_prefix, False)
        visit(node.right, child_prefix, True)

    elif isinstance(node, Identifier):
        print(
            prefix
            + connector
            + f"Identifier({node.name})"
        )

    elif isinstance(node, IntegerLiteral):
        print(
            prefix
            + connector
            + f"IntegerLiteral({node.value})"
        )

    elif isinstance(node, BooleanLiteral):
        print(
            prefix
            + connector
            + f"BooleanLiteral({node.value})"
        )

    elif isinstance(node, CharacterLiteral):
        print(
            prefix
            + connector
            + f"CharacterLiteral('{node.value}')"
        )

    elif isinstance(node, StringLiteral):
        print(
            prefix
            + connector
            + f"StringLiteral('{node.value}')"
        )