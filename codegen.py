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


class CodeGenerator:
    """
    Converts the AST into stack-machine instructions.
    """

    def __init__(self):
        self.instructions = []

    def emit(self, opcode, *operands):
        """Add an instruction and return its index."""
        index = len(self.instructions)
        self.instructions.append((opcode, *operands))
        return index

    def generate(self, program):
        """Generate stack-machine code from the AST."""
        self.instructions = []
        self.visit(program)
        return self.instructions

    def visit(self, node):

        if isinstance(node, Program):
            for statement in node.statements:
                self.visit(statement)

        elif isinstance(node, Declaration):
            self.visit(node.value)
            self.emit("STORE", node.name)

        elif isinstance(node, IfStatement):
            self.visit(node.condition)

            jump_if_false = self.emit("JUMP_IF_FALSE", None)

            for statement in node.then_block:
                self.visit(statement)

            if node.else_block is not None:
                jump_to_end = self.emit("JUMP", None)

                else_start = len(self.instructions)

                self.instructions[jump_if_false] = (
                    "JUMP_IF_FALSE",
                    else_start,
                )

                for statement in node.else_block:
                    self.visit(statement)

                end = len(self.instructions)

                self.instructions[jump_to_end] = (
                    "JUMP",
                    end,
                )

            else:
                end = len(self.instructions)

                self.instructions[jump_if_false] = (
                    "JUMP_IF_FALSE",
                    end,
                )

        elif isinstance(node, PrintStatement):
            for argument in node.arguments:
                self.visit(argument)

            self.emit("PRINT", len(node.arguments))

        elif isinstance(node, BinaryExpression):
            self.visit(node.left)
            self.visit(node.right)

            if node.operator == "+":
                self.emit("ADD")

            elif node.operator == ">":
                self.emit("GT")

            else:
                raise Exception(
                    f"Code Generation Error: "
                    f"Unsupported operator '{node.operator}'"
                )

        elif isinstance(node, Identifier):
            self.emit("LOAD", node.name)

        elif isinstance(node, IntegerLiteral):
            self.emit("PUSH", node.value)

        elif isinstance(node, StringLiteral):
            self.emit("PUSH", node.value)

        else:
            raise Exception(
                f"Code Generation Error: "
                f"Unsupported AST node: {type(node).__name__}"
            )