from aocd import get_data, submit

from collections import deque


def get_dest_label(label, buff, mn, mx):
    while label in buff:
        label -= 1
        if label < mn:
            label = mx
    return label


def insert_three(d, dest_label, buff):
    next_label = d[dest_label]
    d[dest_label] = buff[0]
    d[buff[-1]] = next_label


def iterate(d, current, mn=1, mx=9, p=False):
    dest_label = current - 1
    if dest_label < mn:
        dest_label = mx
    buff, next_label = cut_next_three(d, current)
    dest_label = get_dest_label(dest_label, buff, mn, mx)
    insert_three(d, dest_label, buff)
    return d[current]


def cut_next_three(d, starting_label):
    excised_label = d[starting_label]
    middle_label = d[excised_label]
    last_excised_label = d[middle_label]
    next_label = d[last_excised_label]
    d[starting_label] = next_label
    return (excised_label, middle_label, last_excised_label), next_label


def create_initial(d):
    last_label = d[-1]
    first_label = d[0]
    d = {label: next_label for label, next_label in zip(d, d[1:] + [d[0]])}
    d[last_label] = first_label
    return d


def find_answer(d, starting=1):
    answer = ""
    next_label = d[starting]
    answer += str(next_label)
    while next_label != starting:
        next_label = d[next_label]
        answer += str(next_label)
    return answer[:-1]


def print_n(d, n, starting):
    print()
    print(starting)
    for _ in range(n):
        starting = d[starting]
        print(starting)


def find_answer_b(d, starting=1):
    next_1 = d[starting]
    next_2 = d[next_1]
    print(next_1, next_2, next_1 * next_2)
    return next_1 * next_2


if __name__ == "__main__":
    data = list(map(int, get_data(day=23)))

    current = data[0]
    d1 = create_initial(data)
    d2 = create_initial(data + list(range(10, 1_000_001)))

    for _ in range(100):
        current = iterate(d1, current)
    answer_a = find_answer(d1)
    submit(answer_a, part="a", day=23, year=2020)

    current = data[0]
    for i in range(10_000_000):
        current = iterate(d2, current, mn=1, mx=1_000_000)

    answer_b = find_answer_b(d2)
    submit(answer_b, part="b", day=23, year=2020)
