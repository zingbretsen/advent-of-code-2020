import re
from operator import add, mul

from aocd import get_data, submit


def find_matching_paren(equation):
    buffer = 0
    for i, char in enumerate(equation):
        if char == ")":
            buffer -= 1
        elif char == "(":
            buffer += 1
        if buffer == 0:
            return i


operations = {"*": mul, "+": add}


def parse_equation(equation):
    lhs = 0
    op = add
    i = 0
    l = len(equation)
    rhs = ""
    while i < l:
        char = equation[i]
        if char == "(":
            j = i + find_matching_paren(equation[i:])
            rhs = parse_equation(equation[i + 1 : j])
            lhs = op(lhs, int(rhs))
            rhs = ""
            i = j + 1
        elif char in "+*":
            op = operations[char]
        elif char in "0123456789":
            rhs += char
        else:
            if rhs:
                lhs = op(lhs, int(rhs))
                rhs = ""
        i += 1
    if equation[-1] != ")":
        lhs = op(lhs, int(rhs))
    return lhs


def reduce_parens(equation):
    while "(" in equation:
        for i, char in enumerate(equation):
            if char == "(":
                j = i + find_matching_paren(equation[i:])
                equation = (
                    equation[:i]
                    + str(parse_equation_advanced(equation[i + 1 : j]))
                    + equation[j + 1 :]
                )
                break
    return equation


def reduce_additions(equation):
    while "+" in equation:
        match = re.search(string=equation, pattern="([0-9]+ \+ [0-9]+)")
        start = match.start()
        end = match.end()
        num = parse_equation(equation[start:end])
        equation = equation[:start] + str(num) + equation[end:]
    return equation


def parse_equation_advanced(equation):
    equation = reduce_parens(equation)
    equation = reduce_additions(equation)
    return parse_equation(equation)


if __name__ == "__main__":
    lines = get_data().split("\n")

    answer_a = sum(parse_equation(e) for e in lines)
    submit(answer_a, part="a", day=18, year=2020)

    answer_b = sum(parse_equation_advanced(e) for e in lines)
    submit(answer_b, part="b", day=18, year=2020)
