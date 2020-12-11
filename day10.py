import math
from aocd import get_data, submit


def find_diffs(inputs):
    inputs = sorted(inputs)
    diffs = [inputs[0]]
    for x, y in zip(inputs[:-1], inputs[1:]):
        diffs.append(y - x)
    diffs.append(3)
    return diffs


def find_spans(diffs):
    diffs = [str(n) for n in diffs]
    s = [len(ones) for ones in "".join(diffs).split("3")]

    # These mappings turn out to be the Fibonacci sequence,
    # but using the 3 previous values instead of the previous 2
    mappings = {0: 1, 1: 1, 2: 2, 3: 4, 4: 7}
    s = [mappings[x] for x in s]
    return s


if __name__ == "__main__":
    d = get_data()
    inputs = [int(line) for line in d.split("\n") if line]
    diffs = find_diffs(inputs)

    answer_a = diffs.count(1) * diffs.count(3)
    submit(answer_a, part="a", day=10, year=2020)

    s = find_spans(diffs)
    answer_b = math.prod(s)
    submit(answer_b, part="b", day=10, year=2020)
