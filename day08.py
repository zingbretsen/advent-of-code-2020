from aocd import get_data, submit


def parse_line(line):
    """Pulls out instructions and numbers"""
    instr, num = line.split()
    return instr, int(num)


def find_acc(inputs):
    """Returns the value of the accumulator if input loops or exits"""
    acc = i = 0
    length = len(inputs)
    visited = set()

    while True:
        visited.add(i)

        instr, num = inputs[i]
        delta = 1
        if instr == "acc":
            acc += num
        elif instr == "jmp":
            delta = num

        i += delta
        if i in visited or i == length:
            return acc, i


def flip(inputs):
    """Yields every version of inputs with one jmp/nop flipped"""
    yield inputs
    for i, inp in enumerate(inputs):
        if inp[0] == "acc":
            continue

        modified_inputs = inputs[:]
        if inp[0] == "jmp":
            modified_inputs[i] = ("nop", inp[1])
        else:
            modified_inputs[i] = ("jmp", inp[1])
        yield modified_inputs


def find_full_execution(inputs):
    """Finds the one flipped version that exits successfully"""
    length = len(inputs)
    for modified_inputs in flip(inputs):
        acc, i = find_acc(modified_inputs)
        if length == i:
            return acc


if __name__ == "__main__":
    d = get_data()
    inputs = [parse_line(line) for line in d.split("\n")]

    answer_a, _ = find_acc(inputs)
    submit(answer_a, part="a", day=8, year=2020)

    answer_b = find_full_execution(inputs)
    submit(answer_b, part="b", day=8, year=2020)
