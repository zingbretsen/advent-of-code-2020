from aocd import get_data, submit


def parse_line(line):
    row, col = line[:-3], line[-3:]
    row = row.replace("F", "0").replace("B", "1")
    col = col.replace("L", "0").replace("R", "1")
    return int(row, 2), int(col, 2)


def find_seat(seats):
    seats = sorted(seats)
    prev_seat = seats[0]
    for seat in seats[1:]:
        if seat - 1 != prev_seat:
            return seat - 1
        prev_seat = seat


def get_seat_ids(seats):
    return [row * 8 + col for row, col in seats]


if __name__ == "__main__":
    d = get_data()
    inputs = [parse_line(line) for line in d.split("\n")]

    answer_a = max(row * 8 + col for row, col in inputs)
    submit(answer_a, part="a", day=5, year=2020)

    seats = get_seat_ids(inputs)
    answer_b = find_seat(seats)

    print(answer_b)
    submit(answer_b, part="b", day=5, year=2020)
