from aocd import get_data, submit

from collections import deque


def get_dest_label(label, buff, mn, mx):
    while label in buff:
        label -= 1
        if label < mn:
            label = mx
    return label


def get_dest_idx(d, label):
    return d.index(label) + 1


def iterate(d, mn=1, mx=9, **kwargs):
    dest_label = d[0] - 1
    if dest_label < mn:
        dest_label = mx
    d.rotate(-1)
    buff = []
    for _ in range(3):
        buff.append(d.popleft())
    dest_label = get_dest_label(dest_label, buff, mn, mx)
    dest_idx = get_dest_idx(d, dest_label, **kwargs)
    for b in reversed(buff):
        d.insert(dest_idx, b)


if __name__ == "__main__":

    d = get_data(day=23)
    d = deque(map(int, d))

    for _ in range(100):
        iterate(d)
    while d[0] != 1:
        d.rotate(1)
    answer_a = int("".join(map(str, list(d)[1:])))
    print(answer_a)

    submit(answer_a, part="a", day=23, year=2020)
