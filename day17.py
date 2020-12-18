from aocd import get_data, submit

import itertools
import math


def count_neighbors(grid, i, j, k):
    count = 0
    for cell in itertools.product(*map(lambda x: range(x - 1, x + 2), (i, j, k))):
        if cell == (i, j, k):
            continue
        if cell in grid:
            count += 1
    return count


def get_dims(grid, n_dims=3):
    return [[g[n] for g in grid] for n in range(n_dims)]


def iterate(grid, n_neighbors=3):
    new_grid = grid.copy()
    x, y, z = get_dims(grid)
    min_x, min_y, min_z = map(min, [x, y, z])
    max_x, max_y, max_z = map(max, [x, y, z])
    for i in range(min_x - 1, max_x + 2):
        for j in range(min_y - 1, max_y + 2):
            for k in range(min_z - 1, max_z + 2):
                cell = (i, j, k)
                neighbors = count_neighbors(grid, *cell)
                if cell in grid:
                    if neighbors not in (2, 3):
                        new_grid.remove(cell)
                elif neighbors == 3:
                    new_grid.add(cell)
    return new_grid


def print_grid(grid):
    x, y, z = get_dims(grid)
    min_x, min_y, min_z = map(min, [x, y, z])
    max_x, max_y, max_z = map(max, [x, y, z])
    for k in range(min_z, max_z + 1):
        print(f"z={k}")
        for i in range(min_x, max_x + 1):
            row = ""
            for j in range(min_y, max_y + 1):
                cell = (i, j, k)
                row = row + ("#" if cell in grid else ".")
            print(row)
        print()


if __name__ == "__main__":
    rows = get_data().split()
    rows = """.#.
..#
###""".split()
    # Only store active cells
    grid = {
        (i, j, 0)
        for i, row in enumerate(rows)
        for j, point in enumerate(row)
        if point == "#"
    }

    for _ in range(6):
        grid = iterate(grid)
        print_grid(grid)

    answer_a = len(grid)
    print(answer_a)
    submit(answer_a, part="a", day=17, year=2020)
    answer_b = find_nth_num(nums, 30000000)
    submit(answer_b, part="b", day=17, year=2020)
