from functools import reduce

from aocd import get_data, submit


def count_trees(rows, delta_x, delta_y):
    n_rows = len(rows)
    pos_x = pos_y = 0

    n_trees = 0
    width = len(rows)
    while pos_y < n_rows:
        if rows[pos_y][pos_x] == "#":
            n_trees += 1
            pos_x = (pos_x + delta_x) % width
            pos_y += delta_y
    return n_trees


if __name__ == "__main__":
    d = get_data(day=3, year=2020)
    inputs = [line for line in d.split("\n")]

    answer_a = count_trees(inputs, 3, 1)
    submit(answer_a, part="a", day=3, year=2020)

    n_trees = []
    deltas = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    n_trees = [count_trees(inputs, x, y) for x, y in deltas]
    answer_b = reduce(lambda a, b: a * b, n_trees, 1)
    submit(answer_b, part="b", day=3, year=2020)
