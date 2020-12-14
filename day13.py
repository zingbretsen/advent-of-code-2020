import numpy as np
from aocd import get_data, submit


def find_dep_time(current_time, bus_id):
    dep_time = 0
    while dep_time < current_time:
        dep_time += bus_id
    return dep_time


def find_u(y, mod):
    y = int(y)
    mod = int(mod)
    print(y, mod)
    u = 0
    while (y * u) % mod != 1:
        u += 1
        print(u)
    return u


def find_mod(ns, mods):
    N = ns.prod()
    ys = N / ns
    us = np.array([find_u(y, n) for y, n in zip(ys, ns)])
    return ((mods * ys * us).sum()) % N


def find_answer_b(time_table):
    """Uses Chinese Remainder Theorem to find an N that satisfies given mods

    Algorithm adapted from here:
    https://www.dave4math.com/mathematics/chinese-remainder-theorem/
    """
    bus_ids = [
        (i, int(time)) for i, time in enumerate(time_table.split(",")) if time != "x"
    ]

    ns = np.array([bus_id for offset, bus_id in bus_ids], np.int64)
    mods = -1 * np.array([1 + offset for offset, bus_id in bus_ids], np.int64)

    return find_mod(ns, mods)


if __name__ == "__main__":
    d = get_data()
    current_time, time_table = [line for line in d.split("\n") if line]
    current_time = int(current_time)
    bus_ids = [
        (i, int(time)) for i, time in enumerate(time_table.split(",")) if time != "x"
    ]
    dep_times = [find_dep_time(current_time, t) for i, t in bus_ids]
    m = np.argmin(dep_times)
    bus_id = bus_ids[m][1]
    dep_time = dep_times[m]

    answer_a = bus_id * (dep_time - current_time)
    submit(answer_b, part="a", day=13, year=2020)

    answer_b = find_answer_b(time_table)
    submit(answer_b, part="b", day=13, year=2020)
