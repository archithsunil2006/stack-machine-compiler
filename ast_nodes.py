class Program:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements!r})"


class Declaration:
    def __init__(self, data_type, name, value):
        self.data_type = data_type
        self.name = name
        self.value = value

    def __repr__(self):
        return (
            f"Declaration("
            f"type={self.data_type!r}, "
            f"name={self.name!r}, "
            f"value={self.value!r})"
        )


class IfStatement:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self):
        return (
            f"IfStatement("
            f"condition={self.condition!r}, "
            f"then={self.then_block!r}, "
            f"else={self.else_block!r})"
        )


class PrintStatement:
    def __init__(self, arguments):
        self.arguments = arguments

    def __repr__(self):
        return f"Print({self.arguments!r})"


class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (
            f"BinaryExpression("
            f"left={self.left!r}, "
            f"operator={self.operator!r}, "
            f"right={self.right!r})"
        )


class Identifier:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name!r})"


class IntegerLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"IntegerLiteral({self.value})"


class StringLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringLiteral({self.value!r})"