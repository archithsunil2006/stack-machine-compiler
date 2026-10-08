class StackVM:
    """
    Executes stack-machine instructions.

    The VM maintains:
    - an evaluation stack
    - a variable store
    - an instruction pointer (IP)
    """

    def __init__(self, instructions):
        self.instructions = instructions
        self.stack = []
        self.variables = {}
        self.ip = 0
        self.trace = []

    def run(self):
        """Execute instructions until the program ends."""

        while self.ip < len(self.instructions):
            instruction = self.instructions[self.ip]
            opcode = instruction[0]
            operands = instruction[1:]

            old_ip = self.ip

            # -------------------------
            # Push a constant
            # -------------------------
            if opcode == "PUSH":
                self.stack.append(operands[0])
                self.ip += 1

            # -------------------------
            # Load a variable
            # -------------------------
            elif opcode == "LOAD":
                name = operands[0]

                if name not in self.variables:
                    raise RuntimeError(
                        f"Runtime Error: Variable '{name}' "
                        f"has not been initialized"
                    )

                self.stack.append(self.variables[name])
                self.ip += 1

            # -------------------------
            # Store a variable
            # -------------------------
            elif opcode == "STORE":
                name = operands[0]

                if not self.stack:
                    raise RuntimeError(
                        "Runtime Error: Stack underflow during STORE"
                    )

                self.variables[name] = self.stack.pop()
                self.ip += 1

            # -------------------------
            # Addition
            # -------------------------
            elif opcode == "ADD":
                if len(self.stack) < 2:
                    raise RuntimeError(
                        "Runtime Error: Stack underflow during ADD"
                    )

                right = self.stack.pop()
                left = self.stack.pop()

                self.stack.append(left + right)
                self.ip += 1

            # -------------------------
            # Greater-than comparison
            # -------------------------
            elif opcode == "GT":
                if len(self.stack) < 2:
                    raise RuntimeError(
                        "Runtime Error: Stack underflow during GT"
                    )

                right = self.stack.pop()
                left = self.stack.pop()

                self.stack.append(left > right)
                self.ip += 1

            # -------------------------
            # Conditional jump
            # -------------------------
            elif opcode == "JUMP_IF_FALSE":
                if not self.stack:
                    raise RuntimeError(
                        "Runtime Error: Stack underflow "
                        "during JUMP_IF_FALSE"
                    )

                condition = self.stack.pop()
                target = operands[0]

                if not condition:
                    self.ip = target
                else:
                    self.ip += 1

            # -------------------------
            # Unconditional jump
            # -------------------------
            elif opcode == "JUMP":
                self.ip = operands[0]

            # -------------------------
            # Print values
            # -------------------------
            elif opcode == "PRINT":
                count = operands[0]

                if len(self.stack) < count:
                    raise RuntimeError(
                        "Runtime Error: Stack underflow during PRINT"
                    )

                values = self.stack[-count:]
                del self.stack[-count:]

                print("".join(str(value) for value in values))

                self.ip += 1

            else:
                raise RuntimeError(
                    f"Runtime Error: Unknown instruction '{opcode}'"
                )

            # Record execution state after the instruction.
            self.trace.append(
                {
                    "ip": old_ip,
                    "instruction": instruction,
                    "stack": self.stack.copy(),
                    "variables": self.variables.copy(),
                    "next_ip": self.ip,
                }
            )

        return self.trace

    def print_trace(self):
        """Display the execution trace."""

        print("\nEXECUTION TRACE")
        print("-" * 70)

        for step in self.trace:
            print(
                f"IP={step['ip']:03}  "
                f"{step['instruction']!r:<30} "
                f"Stack={step['stack']}"
            )