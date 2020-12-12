import math
from collections import defaultdict

from aocd import get_data, submit


def find_diffs(inputs):
    inputs = sorted(inputs)
    diffs = inputs[:1]
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


def find_seats(inputs):
    seats = dict()
    for i, row in enumerate(inputs):
        seats[i] = dict()
        for j, location in enumerate(row):
            if location == "L":
                seats[i][j] = 0
    return seats


def get_seat_value(seats, row, col):
    return seats.get(row, dict()).get(col, 0)


def get_surrounding_seat_values(seats, row, col):
    values = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if not (i == 0 and j == 0):
                values.append(get_seat_value(seats, row + i, col + j))
    return values


from copy import deepcopy


def iterate(seats):
    new_seats = seats.deepcopy()
    for i in seats.keys():
        for j in seats[i].keys():
            print(
                i,
                j,
                get_seat_value(seats, i, j),
                get_surrounding_seat_values(seats, i, j),
            )
            if sum(get_surrounding_seat_values(seats, i, j)) == 0:
                new_seats[i][j] = 1
    return new_seats


def print_seats(seats, rows=10, cols=10):
    print()
    for i in range(rows):
        vals = []
        for j in range(cols):
            seat = seats[i].get(j, None)
            if seat in (0, 1):
                vals.append(str(seat))
            else:
                vals.append(".")
        print("".join(vals))


if __name__ == "__main__":
    # d = get_data()
    d = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

    inputs = [line for line in d.split("\n")]
    seats = find_seats(inputs)
    print_seats(seats)
    seats = iterate(seats)
    print_seats(seats)

    answer_a = diffs.count(1) * diffs.count(3)
    submit(answer_a, part="a", day=10, year=2020)

    s = find_spans(diffs)
    answer_b = math.prod(s)
    submit(answer_b, part="b", day=10, year=2020)
