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


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position]

    def advance(self):
        self.position += 1

    def match(self, token_type):
        if self.current_token().token_type == token_type:
            token = self.current_token()
            self.advance()
            return token
        return None

    def expect(self, token_type):
        token = self.current_token()

        if token.token_type != token_type:
            raise Exception(
                f"Syntax Error at line {token.line}: "
                f"Expected {token_type.name}, "
                f"found {token.token_type.name}"
            )

        self.advance()
        return token

    def parse(self):
        statements = []

        while self.current_token().token_type != TokenType.EOF:
            statements.append(self.parse_statement())

        return Program(statements)

    def parse_statement(self):
        token_type = self.current_token().token_type

        if token_type == TokenType.NUM:
            return self.parse_declaration()

        if token_type == TokenType.IF:
            return self.parse_if_statement()

        if token_type == TokenType.PRINT:
            return self.parse_print_statement()

        raise Exception(
            f"Syntax Error at line {self.current_token().line}: "
            f"Unexpected token "
            f"{self.current_token().token_type.name}"
        )

    def parse_declaration(self):
        self.expect(TokenType.NUM)

        name = self.expect(TokenType.IDENTIFIER)

        self.expect(TokenType.ASSIGN)

        value = self.parse_expression()

        self.expect(TokenType.SEMICOLON)

        return Declaration(
            "num",
            name.lexeme,
            value
        )

    def parse_if_statement(self):
        self.expect(TokenType.IF)

        self.expect(TokenType.LPAREN)

        condition = self.parse_expression()

        self.expect(TokenType.RPAREN)

        then_block = self.parse_block()

        else_block = None

        if self.match(TokenType.ELSE):
            else_block = self.parse_block()

        return IfStatement(
            condition,
            then_block,
            else_block
        )

    def parse_block(self):
        self.expect(TokenType.LBRACE)

        statements = []

        while (
            self.current_token().token_type
            != TokenType.RBRACE
        ):
            if self.current_token().token_type == TokenType.EOF:
                raise Exception(
                    f"Syntax Error at line "
                    f"{self.current_token().line}: "
                    "Expected '}'"
                )

            statements.append(self.parse_statement())

        self.expect(TokenType.RBRACE)

        return statements

    def parse_print_statement(self):
        self.expect(TokenType.PRINT)

        arguments = []

        if self.match(TokenType.LPAREN):
            arguments.append(self.parse_expression())

            while self.match(TokenType.COMMA):
                arguments.append(self.parse_expression())

            self.expect(TokenType.RPAREN)
        else:
            # Backward-compatible form: print <expr>; with no parens
            arguments.append(self.parse_expression())

        self.expect(TokenType.SEMICOLON)

        return PrintStatement(arguments)

    def parse_expression(self):
        expression = self.parse_primary()

        while self.current_token().token_type in (
            TokenType.PLUS,
            TokenType.GREATER,
        ):
            operator = self.current_token()
            self.advance()

            right = self.parse_primary()

            expression = BinaryExpression(
                expression,
                operator.lexeme,
                right
            )

        return expression

    def parse_primary(self):
        token = self.current_token()

        if token.token_type == TokenType.INTEGER:
            self.advance()
            return IntegerLiteral(int(token.lexeme))

        if token.token_type == TokenType.STRING:
            self.advance()
            return StringLiteral(token.lexeme)

        if token.token_type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(token.lexeme)

        if token.token_type == TokenType.LPAREN:
            self.advance()

            expression = self.parse_expression()

            self.expect(TokenType.RPAREN)

            return expression

        raise Exception(
            f"Syntax Error at line {token.line}: "
            f"Expected expression, "
            f"found {token.token_type.name}"
        )