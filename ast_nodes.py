class Program:
    def __init__(self, statements):
        self.statements = statements


class Declaration:
    def __init__(self, data_type, name, value):
        self.data_type = data_type
        self.name = name
        self.value = value


class Assignment:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class IfStatement:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class LoopStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class PrintStatement:
    def __init__(self, arguments):
        self.arguments = arguments


class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Identifier:
    def __init__(self, name):
        self.name = name


class IntegerLiteral:
    def __init__(self, value):
        self.value = value


class BooleanLiteral:
    def __init__(self, value):
        self.value = value


class CharacterLiteral:
    def __init__(self, value):
        self.value = value


class StringLiteral:
    def __init__(self, value):
        self.value = value