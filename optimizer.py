def optimize(instructions):
    """
    Run all optimization passes while preserving control-flow
    correctness.
    """

    instructions = constant_folding(instructions)
    instructions = constant_condition_optimization(instructions)
    instructions = remove_redundant_jumps(instructions)

    return instructions


def constant_folding(instructions):
    """
    Fold constant arithmetic and comparison expressions.

    Examples:

        PUSH 2
        PUSH 3
        ADD

    becomes:

        PUSH 5

    and:

        PUSH 2
        PUSH 1
        GT

    becomes:

        PUSH True
    """

    result = []
    mapping = {}

    i = 0

    while i < len(instructions):

        # Constant ADD
        if (
            i + 2 < len(instructions)
            and instructions[i][0] == "PUSH"
            and instructions[i + 1][0] == "PUSH"
            and instructions[i + 2][0] == "ADD"
        ):
            left = instructions[i][1]
            right = instructions[i + 1][1]

            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                new_index = len(result)

                mapping[i] = new_index
                mapping[i + 1] = new_index
                mapping[i + 2] = new_index

                result.append(("PUSH", left + right))

                i += 3
                continue

        # Constant GT
        if (
            i + 2 < len(instructions)
            and instructions[i][0] == "PUSH"
            and instructions[i + 1][0] == "PUSH"
            and instructions[i + 2][0] == "GT"
        ):
            left = instructions[i][1]
            right = instructions[i + 1][1]

            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                new_index = len(result)

                mapping[i] = new_index
                mapping[i + 1] = new_index
                mapping[i + 2] = new_index

                result.append(("PUSH", left > right))

                i += 3
                continue

        mapping[i] = len(result)
        result.append(instructions[i])

        i += 1

    return remap_targets(result, mapping, len(instructions))


def constant_condition_optimization(instructions):
    """
    Optimize constant conditional branches.

    PUSH True + JUMP_IF_FALSE
        -> remove both

    PUSH False + JUMP_IF_FALSE target
        -> JUMP target
    """

    result = []
    mapping = {}

    i = 0

    while i < len(instructions):

        if (
            i + 1 < len(instructions)
            and instructions[i][0] == "PUSH"
            and instructions[i + 1][0] == "JUMP_IF_FALSE"
            and isinstance(instructions[i][1], bool)
        ):
            condition = instructions[i][1]
            target = instructions[i + 1][1]

            new_index = len(result)

            mapping[i] = new_index
            mapping[i + 1] = new_index

            if condition is False:
                result.append(("JUMP", target))

            # If True, both instructions are removed.

            i += 2
            continue

        mapping[i] = len(result)
        result.append(instructions[i])

        i += 1

    return remap_targets(result, mapping, len(instructions))


def remove_redundant_jumps(instructions):
    """
    Remove unconditional jumps that already point to the
    immediately following instruction.
    """

    result = []
    mapping = {}

    i = 0

    while i < len(instructions):

        instruction = instructions[i]

        if instruction[0] == "JUMP" and instruction[1] == i + 1:
            mapping[i] = len(result)
            i += 1
            continue

        mapping[i] = len(result)
        result.append(instruction)

        i += 1

    return remap_targets(result, mapping, len(instructions))


def remap_targets(instructions, mapping, old_length):
    """
    Convert jump targets from old instruction indices to
    new instruction indices.

    If a jump targets an instruction that was removed,
    find the next surviving instruction.
    """

    # Build a function that finds the new location corresponding
    # to an old instruction.
    def translate(target):
        if target >= old_length:
            return len(instructions)

        if target in mapping:
            return mapping[target]

        # Target instruction was removed.
        # Find the next surviving instruction.
        current = target

        while current < old_length:
            if current in mapping:
                return mapping[current]
            current += 1

        return len(instructions)

    result = []

    for instruction in instructions:

        opcode = instruction[0]

        if opcode in ("JUMP", "JUMP_IF_FALSE"):
            target = translate(instruction[1])
            result.append((opcode, target))
        else:
            result.append(instruction)

    return result

class PeepholeOptimizer:
    def optimize(self, instructions):
        return optimize(instructions)