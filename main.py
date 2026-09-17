from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from ast_printer import print_ast


SOURCE_FILE = "test.txt"


def print_tokens(tokens):
    print("\nTOKENS")
    print("-" * 55)

    print(
        f"{'TOKEN':<15}"
        f"{'LEXEME':<20}"
        f"{'LINE':<10}"
    )

    print("-" * 55)

    for token in tokens:
        print(
            f"{token.token_type.name:<15}"
            f"{token.lexeme!r:<20}"
            f"{token.line:<10}"
        )



def main():
    print("=== Compiler Prototype ===")

    try:
        # Read source program from external file
        with open(SOURCE_FILE, "r") as file:
            source_code = file.read()

        # Stage 1: Lexical Analysis
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        print_tokens(tokens)

        # Stage 2: Syntax Analysis
        parser = Parser(tokens)
        ast = parser.parse()

        print("\nAST")
        print("-" * 40)
        print_ast(ast)

        # Stage 3: Semantic Analysis
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(ast)

        print("\nSEMANTIC ANALYSIS")
        print("-" * 40)

        if errors:
            for error in errors:
                print(error)
        else:
            print("No semantic errors detected.")

    except FileNotFoundError:
        print(f"Error: Source file '{SOURCE_FILE}' not found.")

    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()