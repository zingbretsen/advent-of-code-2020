from itertools import combinations
from aocd import get_data, submit


def find_sum_combs(inputs, total=2020, n=2):
    for comb in combinations(inputs, n):
        if sum(comb) == total:
            return comb


if __name__ == '__main__':
    d = get_data(day=1, year=2020)
    inputs = [int(line) for line in d.split('\n')]

    x, y = find_sum_combs(inputs)
    submit(x*y, part='a', day=1, year=2020)

    x, y, z = find_sum_combs(inputs, n=3)
    submit(x*y*z, part='b', day=1, year=2020)
