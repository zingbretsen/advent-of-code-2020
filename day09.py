from itertools import combinations
from aocd import get_data, submit


def find_sum(lst, num, n=2):
    for comb in combinations(lst, n):
        if sum(comb) == num:
            return True
    return False


def find_a(lst, preamble=25, n=2):
    i = preamble
    while True:
        if find_sum(lst[i - preamble : i], lst[i]):
            i += 1
        else:
            return lst[i]


def find_contiguous(lst, target):
    i = 0
    j = i + 2
    total = 0
    while total != target:
        total = sum(lst[i:j])
        if total < target:
            j += 1
        if total > target:
            i += 1
            j = i + 2

    return min(lst[i:j]) + max(lst[i:j])


if __name__ == "__main__":
    d = get_data()
    inputs = [int(line) for line in d.split("\n")]

    answer_a = find_a(inputs)
    submit(answer_a, part="a", day=9, year=2020)

    answer_b = find_contiguous(inputs, answer_a)
    submit(answer_b, part="b", day=9, year=2020)
