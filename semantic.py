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

from symbol_table import SymbolTable


class SemanticAnalyzer:

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []

    def analyze(self, program):
        self.symbol_table = SymbolTable()
        self.errors = []

        self.visit(program)

        return self.errors

    def visit(self, node):

        if isinstance(node, Program):
            for statement in node.statements:
                self.visit(statement)

        elif isinstance(node, Declaration):
            value_type = self.visit(node.value)

            if value_type is not None and value_type != node.data_type:
                self.errors.append(
                    f"Semantic Error: Cannot assign "
                    f"{value_type} to {node.data_type} "
                    f"variable '{node.name}'"
                )

            if not self.symbol_table.declare(
                node.name,
                node.data_type
            ):
                self.errors.append(
                    f"Semantic Error: Variable "
                    f"'{node.name}' has already been declared"
                )

        elif isinstance(node, Assignment):
            variable_type = self.symbol_table.lookup(node.name)

            if variable_type is None:
                self.errors.append(
                    f"Semantic Error: Variable "
                    f"'{node.name}' has not been declared"
                )
                self.visit(node.value)
                return

            value_type = self.visit(node.value)

            if value_type is not None and value_type != variable_type:
                self.errors.append(
                    f"Semantic Error: Cannot assign "
                    f"{value_type} to {variable_type} "
                    f"variable '{node.name}'"
                )

        elif isinstance(node, IfStatement):
            condition_type = self.visit(node.condition)

            if condition_type != "bool":
                self.errors.append(
                    "Semantic Error: If condition must be boolean"
                )

            for statement in node.then_block:
                self.visit(statement)

            if node.else_block is not None:
                for statement in node.else_block:
                    self.visit(statement)

        elif isinstance(node, LoopStatement):
            condition_type = self.visit(node.condition)

            if condition_type != "bool":
                self.errors.append(
                    "Semantic Error: Loop condition must be boolean"
                )

            for statement in node.body:
                self.visit(statement)

        elif isinstance(node, PrintStatement):
            for argument in node.arguments:
                self.visit(argument)

        elif isinstance(node, BinaryExpression):
            left_type = self.visit(node.left)
            right_type = self.visit(node.right)

            if node.operator in ("+", "-"):
                if left_type == "num" and right_type == "num":
                    return "num"

                self.errors.append(
                    f"Semantic Error: '{node.operator}' "
                    "requires numeric operands"
                )
                return None

            if node.operator == ">":
                if left_type == "num" and right_type == "num":
                    return "bool"

                self.errors.append(
                    "Semantic Error: '>' requires numeric operands"
                )
                return None

            self.errors.append(
                f"Semantic Error: Unsupported operator "
                f"'{node.operator}'"
            )
            return None

        elif isinstance(node, Identifier):
            data_type = self.symbol_table.lookup(node.name)

            if data_type is None:
                self.errors.append(
                    f"Semantic Error: Variable "
                    f"'{node.name}' has not been declared"
                )
                return None

            return data_type

        elif isinstance(node, IntegerLiteral):
            return "num"

        elif isinstance(node, BooleanLiteral):
            return "bool"

        elif isinstance(node, CharacterLiteral):
            return "letter"

        elif isinstance(node, StringLiteral):
            return "text"

        return None