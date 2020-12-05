from aocd import get_data, submit


def parse_line(line):
    line = line.replace("F", "0").replace("B", "1")
    line = line.replace("L", "0").replace("R", "1")
    return int(line, 2)


def find_seat(seats):
    seats = set(seats)
    all_seats = set(range(min(seats), max(seats)))
    return (all_seats - seats).pop()


if __name__ == "__main__":
    d = get_data()
    inputs = [parse_line(line) for line in d.split("\n")]

    answer_a = max(inputs)
    submit(answer_a, part="a", day=5, year=2020)

    answer_b = find_seat(inputs)
    submit(answer_b, part="b", day=5, year=2020)
