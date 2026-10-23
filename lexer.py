from tokens import Token, TokenType


KEYWORDS = {
    "num": TokenType.NUM,
    "bool": TokenType.BOOL,
    "letter": TokenType.LETTER,
    "text": TokenType.TEXT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "loop": TokenType.LOOP,
    "print": TokenType.PRINT,
}


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1

    def current_char(self):
        if self.position >= len(self.source):
            return None
        return self.source[self.position]

    def advance(self):
        self.position += 1

    def tokenize(self):
        tokens = []

        while self.current_char() is not None:
            char = self.current_char()

            if char in " \t\r":
                self.advance()

            elif char == "\n":
                self.line += 1
                self.advance()

            elif char.isalpha() or char == "_":
                tokens.append(self.read_identifier())

            elif char.isdigit():
                tokens.append(self.read_integer())

            elif char == '"':
                tokens.append(self.read_string())

            elif char == "'":
                tokens.append(self.read_character())

            elif char == "=":
                tokens.append(Token(TokenType.ASSIGN, char, self.line))
                self.advance()

            elif char == "+":
                tokens.append(Token(TokenType.PLUS, char, self.line))
                self.advance()

            elif char == "-":
                tokens.append(Token(TokenType.MINUS, char, self.line))
                self.advance()

            elif char == ">":
                tokens.append(Token(TokenType.GREATER, char, self.line))
                self.advance()

            elif char == "(":
                tokens.append(Token(TokenType.LPAREN, char, self.line))
                self.advance()

            elif char == ")":
                tokens.append(Token(TokenType.RPAREN, char, self.line))
                self.advance()

            elif char == "{":
                tokens.append(Token(TokenType.LBRACE, char, self.line))
                self.advance()

            elif char == "}":
                tokens.append(Token(TokenType.RBRACE, char, self.line))
                self.advance()

            elif char == ";":
                tokens.append(Token(TokenType.SEMICOLON, char, self.line))
                self.advance()

            elif char == ",":
                tokens.append(Token(TokenType.COMMA, char, self.line))
                self.advance()

            else:
                raise Exception(
                    f"Lexical Error at line {self.line}: "
                    f"Unexpected character '{char}'"
                )

        tokens.append(Token(TokenType.EOF, "", self.line))
        return tokens

    def read_identifier(self):
        start = self.position

        while (
            self.current_char() is not None
            and (
                self.current_char().isalnum()
                or self.current_char() == "_"
            )
        ):
            self.advance()

        lexeme = self.source[start:self.position]

        if lexeme in KEYWORDS:
            token_type = KEYWORDS[lexeme]

            if lexeme == "true" or lexeme == "false":
                token_type = TokenType.BOOLEAN
        elif lexeme == "true" or lexeme == "false":
            token_type = TokenType.BOOLEAN
        else:
            token_type = TokenType.IDENTIFIER

        return Token(token_type, lexeme, self.line)

    def read_integer(self):
        start = self.position

        while (
            self.current_char() is not None
            and self.current_char().isdigit()
        ):
            self.advance()

        lexeme = self.source[start:self.position]

        return Token(TokenType.INTEGER, lexeme, self.line)

    def read_string(self):
        start_line = self.line

        self.advance()
        start = self.position

        while (
            self.current_char() is not None
            and self.current_char() != '"'
        ):
            if self.current_char() == "\n":
                self.line += 1

            self.advance()

        if self.current_char() is None:
            raise Exception(
                f"Lexical Error at line {start_line}: "
                "Unterminated string literal"
            )

        lexeme = self.source[start:self.position]
        self.advance()

        return Token(TokenType.STRING, lexeme, start_line)

    def read_character(self):
        start_line = self.line

        self.advance()

        if self.current_char() is None:
            raise Exception(
                f"Lexical Error at line {start_line}: "
                "Unterminated character literal"
            )

        character = self.current_char()
        self.advance()

        if self.current_char() != "'":
            raise Exception(
                f"Lexical Error at line {start_line}: "
                "Character literal must contain exactly one character"
            )

        self.advance()

        return Token(
            TokenType.CHARACTER,
            character,
            start_line
        )