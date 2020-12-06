from collections import Counter
from aocd import get_data, submit


def parse_lines(lines):
    lines = lines.split("\n")
    n_lines = len(lines)

    char_counter = Counter()
    for line in lines:
        char_counter.update(line)

    char_counter = {k: v / n_lines for k, v in char_counter.items()}
    return char_counter


if __name__ == "__main__":
    d = get_data()
    inputs = [parse_lines(lines) for lines in d.split("\n\n")]

    answer_a = sum(len(chars.keys()) for chars in inputs)
    submit(answer_a, part="a", day=6, year=2020)

    answer_b = sum(len([1 for v in chars.values() if v == 1]) for chars in inputs)
    submit(answer_b, part="b", day=6, year=2020)
