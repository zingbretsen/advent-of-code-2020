import math
import numpy as np

from copy import deepcopy
from aocd import get_data, submit


def calc_card_loop(subj, target):
    i = 0
    val = 1
    while val != target:
        i += 1
        val = loop(subj, val)
        # val = gen(7, i)
    return i


def loop(subj, val):
    val *= subj
    val = val % 20201227
    return val


def gen(subj, n_loops):
    val = 1
    for _ in range(n_loops):
        val = loop(subj, val)
    return val


if __name__ == "__main__":
    a, b = map(int, get_data(day=25).split("\n"))
    n1 = calc_card_loop(7, a)
    n2 = calc_card_loop(7, b)

    answer_a = gen(b, n1)
    print(gen(a, n2))
    print(calc_card_loop(7, 5764801))
    print(calc_card_loop(7, 17807724))
    submit(answer_a, part="a", day=25, year=2020)
    # submit(answer_b, part="b", day=25, year=2020)
