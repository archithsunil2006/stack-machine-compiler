from tokens import TokenType
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
from symbol_table import SymbolTable


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []

    def analyze(self, program):
        self.visit_program(program)
        return self.errors

    def visit_program(self, program):
        for statement in program.statements:
            self.visit(statement)

    def visit(self, node):
        if isinstance(node, Declaration):
            return self.visit_declaration(node)

        if isinstance(node, IfStatement):
            return self.visit_if_statement(node)

        if isinstance(node, PrintStatement):
            return self.visit_print_statement(node)

        if isinstance(node, BinaryExpression):
            return self.visit_binary_expression(node)

        if isinstance(node, Identifier):
            return self.visit_identifier(node)

        if isinstance(node, IntegerLiteral):
            return "num"

        if isinstance(node, StringLiteral):
            return "text"

        if isinstance(node, list):
            for statement in node:
                self.visit(statement)

        return None

    def visit_declaration(self, node):
        value_type = self.visit(node.value)

        if not self.symbol_table.declare(
            node.name,
            node.data_type
        ):
            self.errors.append(
                f"Semantic Error: Variable '{node.name}' "
                f"is already declared"
            )
            return

        if value_type is not None and value_type != node.data_type:
            self.errors.append(
                f"Semantic Error: Cannot assign "
                f"{value_type} to {node.data_type} variable "
                f"'{node.name}'"
            )

    def visit_if_statement(self, node):
        condition_type = self.visit(node.condition)

        if condition_type != "bool":
            self.errors.append(
                "Semantic Error: If condition must be boolean"
            )

        self.visit(node.then_block)

        if node.else_block is not None:
            self.visit(node.else_block)

    def visit_print_statement(self, node):
        for argument in node.arguments:
            self.visit(argument)

    def visit_binary_expression(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if node.operator == "+":
            if left_type == "num" and right_type == "num":
                return "num"

            if left_type == "text" and right_type == "text":
                return "text"

            # Coercion rule: concatenating text with a num is allowed,
            # the num operand is implicitly converted to text.
            if left_type == "text" and right_type == "num":
                return "text"

            if left_type == "num" and right_type == "text":
                return "text"

            self.errors.append(
                "Semantic Error: '+' requires operands "
                "of compatible types"
            )
            return None

        if node.operator == ">":
            if left_type == "num" and right_type == "num":
                return "bool"

            self.errors.append(
                "Semantic Error: '>' requires two num operands"
            )
            return None

        self.errors.append(
            f"Semantic Error: Unknown operator '{node.operator}'"
        )
        return None

    def visit_identifier(self, node):
        data_type = self.symbol_table.lookup(node.name)

        if data_type is None:
            self.errors.append(
                f"Semantic Error: Variable '{node.name}' "
                f"has not been declared"
            )
            return None

        return data_type