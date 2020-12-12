import math
from collections import defaultdict

import numpy as np

from aocd import get_data, submit


def find_seats(inputs):
    seat_locations = []
    for i, row in enumerate(inputs):
        for j, location in enumerate(row):
            if location == "L":
                seat_locations.append((i, j))
    return seat_locations


def get_seat_value(seats, row, col):
    return seats.get(row, dict()).get(col, 0)


def get_surrounding_seat_values(seats, row, col):
    values = []
    for i in [-1, 0, 1]:
        i2 = row + i
        for j in [-1, 0, 1]:
            j2 = col + j
            if not (i == 0 and j == 0) and (0 <= i2) and (0 <= j2):
                try:
                    values.append(seats[i2, j2])
                except indexerror:
                    pass
    return values


def find_nearest_los_seat(seats, occupied_seats, i, j, dx, dy):
    """Look in one direction for the nearest seat.

    If you find a seat, return its occupancy status, otherwise return 0.
    """
    n_rows, n_cols = occupied_seats.shape
    while True:
        i += dx
        j += dy
        if i < 0 or j < 0 or i >= n_rows or j >= n_cols:
            return 0
        if (i, j) in seats:
            return occupied_seats[i, j]


def find_los_neighbors(seats, occupied_self, i, j):
    """Finds total occupied seats in line of sight."""
    values = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if not (dx == 0 and dy == 0):
                values.append(
                    find_nearest_los_seat(seats, occupied_seats, i, j, dx, dy)
                )
    return values


def get_line_of_sight_seats(seats, row, col):
    values = []
    for i in [-1, 0, 1]:
        i2 = row + i
        for j in [-1, 0, 1]:
            j2 = col + j
            if not (i == 0 and j == 0) and (0 <= i2) and (0 <= j2):
                try:
                    values.append(seats[i2, j2])
                except indexerror:
                    pass
    return values


from copy import deepcopy


def iterate(seats, occupied_seats, part="a"):
    if part == "a":
        score = get_surrounding_seat_values
        n_neighbors = 4
    else:
        score = find_los_neighbors
        n_neighbors = 5

    new_seats = occupied_seats.copy()
    for i, j in seats:
        if part == "a":
            neighbors = sum(get_surrounding_seat_values(occupied_seats, i, j))
        else:
            neighbors = sum(find_los_neighbors(seats, occupied_seats, i, j))
        if neighbors == 0:
            new_seats[i, j] = 1
        elif neighbors >= n_neighbors:
            new_seats[i, j] = 0
    return new_seats


if __name__ == "__main__":
    d = get_data()
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
    occupied_seats = np.zeros((len(inputs), len(inputs[0])), np.int32)
    for i in range(200):
        occupied_seats = iterate(seats, occupied_seats, part="a")
        print(occupied_seats.sum())

    answer_a = 2251
    submit(answer_a, part="a", day=11, year=2020)

    seats = find_seats(inputs)
    occupied_seats = np.zeros((len(inputs), len(inputs[0])), np.int32)
    for i in range(200):
        occupied_seats = iterate(seats, occupied_seats, part="b")
        print(occupied_seats.sum())

    answer_b = occupied_seats.sum()
    submit(answer_b, part="b", day=11, year=2020)
