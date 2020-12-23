from operator import mul
import math
import numpy as np

from copy import deepcopy
from aocd import get_data, submit


def play_round(p1, p2):
    c1 = p1.pop(0)
    c2 = p2.pop(0)
    if c1 > c2:
        p1.extend((c1, c2))
    else:
        p2.extend((c2, c1))


def play_game(p1, p2):
    p1 = p1.copy()
    p2 = p2.copy()
    visited = set()
    while len(p1) > 0 and len(p2) > 0:
        play_round(p1, p2)

    return p1, p2


def play_game_recursive(p1, p2, recursive=False, game=1):
    p1 = p1.copy()
    p2 = p2.copy()
    visited = set()
    while len(p1) > 0 and len(p2) > 0:
        hsh = (tuple(p1), tuple(p2))
        if hsh in visited:
            return p1, []
        visited.add(hsh)

        # If both can recurse
        if p1[0] < len(p1) and p2[0] < len(p2):
            c1 = p1.pop(0)
            c2 = p2.pop(0)
            sub1, sub2 = play_game_recursive(p1[:c1], p2[:c2], True, game + 1)
            if len(sub1) > len(sub2):
                p1.extend((c1, c2))
            else:
                p2.extend((c2, c1))
        # If at least one player cannot recurse
        else:
            play_round(p1, p2)

    return p1, p2


def score(p1, p2):
    p1.extend(p2)
    p1 = reversed(p1)
    s = sum(mul(c, n) for c, n in enumerate(p1, start=1))
    return s


if __name__ == "__main__":
    d = get_data(day=22)

    p1, p2 = d.split("\n\n")
    p1 = list(map(int, p1.split("\n")[1:]))
    p2 = list(map(int, p2.split("\n")[1:]))

    p1_end, p2_end = play_game(p1, p2)
    answer_a = score(p1_end, p2_end)
    submit(answer_a, part="a", day=22, year=2020)

    p1_end, p2_end = play_game_recursive(p1, p2, True)
    answer_b = score(p1_end, p2_end)
    submit(answer_b, part="b", day=22, year=2020)
