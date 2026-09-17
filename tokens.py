from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    NUM = auto()
    IF = auto()
    ELSE = auto()
    PRINT = auto()

    # Identifiers and literals
    IDENTIFIER = auto()
    INTEGER = auto()
    STRING = auto()

    # Operators
    ASSIGN = auto()
    PLUS = auto()
    GREATER = auto()

    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()

    # End of input
    EOF = auto()


class Token:
    def __init__(self, token_type, lexeme, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line

    def __repr__(self):
        return f"{self.token_type.name}({self.lexeme!r})"