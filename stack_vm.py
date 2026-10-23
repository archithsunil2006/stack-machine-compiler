class StackVM:
    def __init__(self, instructions):
        self.instructions = instructions
        self.stack = []
        self.variables = {}
        self.pc = 0
        self.trace = []

    def run(self):
        while self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            opcode = instruction[0]

            self.trace.append({
                "pc": self.pc,
                "instruction": instruction,
                "stack": self.stack.copy(),
                "variables": self.variables.copy(),
            })

            if opcode == "PUSH":
                self.stack.append(instruction[1])
                self.pc += 1

            elif opcode == "LOAD":
                name = instruction[1]

                if name not in self.variables:
                    raise RuntimeError(
                        f"Variable '{name}' is not defined"
                    )

                self.stack.append(self.variables[name])
                self.pc += 1

            elif opcode == "STORE":
                name = instruction[1]

                if not self.stack:
                    raise RuntimeError(
                        "Stack underflow during STORE"
                    )

                self.variables[name] = self.stack.pop()
                self.pc += 1

            elif opcode == "ADD":
                right = self.stack.pop()
                left = self.stack.pop()

                self.stack.append(left + right)
                self.pc += 1

            elif opcode == "SUB":
                right = self.stack.pop()
                left = self.stack.pop()

                self.stack.append(left - right)
                self.pc += 1

            elif opcode == "GT":
                right = self.stack.pop()
                left = self.stack.pop()

                self.stack.append(left > right)
                self.pc += 1

            elif opcode == "JUMP_IF_FALSE":
                target = instruction[1]
                condition = self.stack.pop()

                if not condition:
                    self.pc = target
                else:
                    self.pc += 1

            elif opcode == "JUMP":
                self.pc = instruction[1]

            elif opcode == "PRINT":
                count = instruction[1]
                values = []

                for _ in range(count):
                    if not self.stack:
                        raise RuntimeError(
                            "Stack underflow during PRINT"
                        )

                    values.append(self.stack.pop())

                values.reverse()
                print(*values)

                self.pc += 1

            else:
                raise RuntimeError(
                    f"Unknown instruction: {opcode}"
                )

        return self.trace

    def print_trace(self):
        print("\nEXECUTION TRACE")
        print("-" * 110)

        print(
            f"{'PC':<5}"
            f"{'Instruction':<30}"
            f"{'Stack':<30}"
            f"{'Variables':<45}"
        )

        print("-" * 110)

        for step in self.trace:
            instruction = step["instruction"]
            opcode = instruction[0]

            if len(instruction) > 1:
                instruction_text = f"{opcode} {instruction[1]}"
            else:
                instruction_text = opcode

            stack_text = str(step["stack"])
            variables_text = str(step["variables"])

            print(
                f"{step['pc']:<5}"
                f"{instruction_text:<30}"
                f"{stack_text:<30}"
                f"{variables_text:<45}"
            )

        print("-" * 110)