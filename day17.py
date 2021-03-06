from aocd import get_data, submit

import itertools


def count_neighbors(grid, orig_cell):
    count = 0
    for cell in itertools.product(*map(lambda x: range(x - 1, x + 2), orig_cell)):
        if cell == orig_cell:
            continue
        if cell in grid:
            count += 1
    return count


def get_dims(grid, n_dims=3):
    return [[g[n] for g in grid] for n in range(n_dims)]


def iterate(grid, n_dims=3):
    new_grid = grid.copy()
    dims = get_dims(grid, n_dims)
    mins = map(min, dims)
    maxes = map(max, dims)
    for cell in itertools.product(
        *[range(mn - 1, mx + 2) for mn, mx in zip(mins, maxes)]
    ):
        neighbors = count_neighbors(grid, cell)
        if cell in grid:
            if neighbors not in (2, 3):
                new_grid.remove(cell)
        elif neighbors == 3:
            new_grid.add(cell)
    return new_grid


def make_grid(rows, n_dims):
    # All but 2 of our dimensions should be 0
    zeros = [0 for _ in range(n_dims - 2)]

    # Only store active cells
    return {
        (i, j, *zeros)
        for i, row in enumerate(rows)
        for j, point in enumerate(row)
        if point == "#"
    }


if __name__ == "__main__":
    rows = get_data().split()

    grid = make_grid(rows, 3)
    for _ in range(6):
        grid = iterate(grid, 3)

    answer_a = len(grid)
    submit(answer_a, part="a", day=17, year=2020)

    grid = make_grid(rows, 4)
    for _ in range(6):
        grid = iterate(grid, 4)

    answer_b = len(grid)
    submit(answer_b, part="b", day=17, year=2020)
