import unittest

from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator
from optimizer import PeepholeOptimizer
from stack_vm import StackVM


def compile_source(source):
    """Run source through the compiler pipeline up to code generation."""

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)

    if errors:
        return None, errors

    generator = CodeGenerator()
    instructions = generator.generate(ast)

    return instructions, []


class CompilerTests(unittest.TestCase):

    def test_arithmetic(self):
        source = """
        num a = 5;
        num b = 2;
        print(a + b);
        """

        instructions, errors = compile_source(source)

        self.assertEqual(errors, [])

        vm = StackVM(instructions)
        trace = vm.run()

        self.assertEqual(vm.stack, [])
        self.assertEqual(vm.variables["a"], 5)
        self.assertEqual(vm.variables["b"], 2)

        self.assertTrue(
            any(
                step["instruction"][0] == "ADD"
                for step in trace
            )
        )

    def test_if_else(self):
        source = """
        num a = 5;
        num b = 2;

        if (a > b) {
            print(a);
        }
        else {
            print(b);
        }
        """

        instructions, errors = compile_source(source)

        self.assertEqual(errors, [])

        vm = StackVM(instructions)
        trace = vm.run()

        self.assertEqual(vm.variables["a"], 5)
        self.assertEqual(vm.variables["b"], 2)

        self.assertTrue(
            any(
                step["instruction"][0] == "JUMP_IF_FALSE"
                for step in trace
            )
        )

    def test_undeclared_variable(self):
        source = """
        print(a);
        """

        instructions, errors = compile_source(source)

        self.assertIsNone(instructions)

        self.assertTrue(
            any(
                "has not been declared" in error
                for error in errors
            )
        )

    def test_type_error(self):
        source = """
        num a = "hello";
        """

        instructions, errors = compile_source(source)

        self.assertIsNone(instructions)

        self.assertTrue(
            any(
                "Cannot assign" in error
                for error in errors
            )
        )

    def test_syntax_error(self):
        source = """
        num a = 5
        """

        with self.assertRaises(Exception):
            lexer = Lexer(source)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            parser.parse()

    def test_runtime_variable_error(self):
        instructions = [
            ("LOAD", "missing"),
        ]

        vm = StackVM(instructions)

        with self.assertRaises(RuntimeError):
            vm.run()

    def test_constant_folding(self):
        instructions = [
            ("PUSH", 2),
            ("PUSH", 3),
            ("ADD",),
        ]

        optimizer = PeepholeOptimizer()
        optimized = optimizer.optimize(instructions)

        self.assertEqual(
            optimized,
            [("PUSH", 5)]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)