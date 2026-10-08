from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from ast_printer import print_ast
from codegen import CodeGenerator
from optimizer import PeepholeOptimizer
from stack_vm import StackVM


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


def print_instructions(title, instructions):
    print(f"\n{title}")
    print("-" * 55)

    for index, instruction in enumerate(instructions):
        print(f"{index:03}: {instruction}")


def main():
    print("=== Compiler Prototype ===")

    try:
        # Read source program
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

            return

        print("No semantic errors detected.")

        # Stage 4: Code Generation
        generator = CodeGenerator()
        instructions = generator.generate(ast)

        print_instructions(
            "GENERATED CODE",
            instructions
        )

        # Stage 5: Peephole Optimization
        optimizer = PeepholeOptimizer()
        optimized_instructions = optimizer.optimize(
            instructions
        )

        print_instructions(
            "OPTIMIZED CODE",
            optimized_instructions
        )

        print(
            f"\nInstruction Count: "
            f"{len(instructions)} -> "
            f"{len(optimized_instructions)}"
        )

        # Stage 6: Stack Machine Execution
        vm = StackVM(optimized_instructions)

        vm.run()

        # Stage 7: Execution Trace
        vm.print_trace()

    except FileNotFoundError:
        print(
            f"Error: Source file '{SOURCE_FILE}' not found."
        )

    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()