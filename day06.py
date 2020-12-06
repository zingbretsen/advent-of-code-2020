from collections import Counter
from aocd import get_data, submit


def parse_lines(lines):
    n_passengers = lines.count("\n") + 1
    lines = lines.replace("\n", "")

    char_counter = Counter(lines)

    return {k: v / n_passengers for k, v in char_counter.items()}


if __name__ == "__main__":
    d = get_data()
    inputs = [parse_lines(lines) for lines in d.split("\n\n")]

    answer_a = sum(len(chars.keys()) for chars in inputs)
    submit(answer_a, part="a", day=6, year=2020)

    answer_b = sum(len([1 for v in chars.values() if v == 1]) for chars in inputs)
    submit(answer_b, part="b", day=6, year=2020)
