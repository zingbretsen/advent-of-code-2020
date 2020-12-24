from aocd import get_data, submit
from collections import Counter

# Half steps are required in the x direction when changing levels
directions = {
    "e": 1,
    "se": 0.5 - 1j,
    "ne": 0.5 + 1j,
    "w": -1,
    "sw": -0.5 - 1j,
    "nw": -0.5 + 1j,
}


def parse_instructions(data):
    instructions = []
    for inst in data:
        i = 0
        movement = 0
        while i < len(inst):
            if inst[i : i + 1] in directions:
                movement += directions[inst[i : i + 1]]
                i += 1
            else:
                movement += directions[inst[i : i + 2]]
                i += 2
        instructions.append(movement)
    return instructions


def find_extent(d):
    minx = int(min(x.real for x in d) * 2) - 1
    maxx = int(max(x.real for x in d) * 2) + 1
    miny = int(min(y.imag for y in d)) - 1
    maxy = int(max(y.imag for y in d)) + 1
    return (minx, maxx), (miny, maxy)


def count_neighbors(cell, d):
    count = 0
    for direction in directions.values():
        if (cell + direction) in d:
            count += 1
    return count


def iterate(d):
    orig_d = d.copy()
    extents = find_extent(d)
    for x in range(extents[0][0], extents[0][1] + 1):
        for y in range(extents[1][0], extents[1][1] + 1):
            cell = x / 2 + y * 1j
            neigh = count_neighbors(cell, orig_d)
            if cell in orig_d:
                if neigh == 0 or neigh > 2:
                    d.remove(cell)
            elif neigh == 2:
                d.add(cell)


if __name__ == "__main__":

    data = get_data(day=24).split("\n")

    cells = parse_instructions(data)
    count = Counter(cells)
    answer_a = 0

    cells2 = set()
    for cell, value in count.items():
        if value % 2 == 1:
            cells2.add(cell)
            answer_a += 1
    submit(answer_a, part="a", day=24, year=2020)

    for _ in range(100):
        iterate(cells2)

    answer_b = len(cells2)
    submit(answer_b, part="b", day=24, year=2020)
