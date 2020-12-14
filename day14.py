import re
from itertools import product
from collections import defaultdict
from aocd import get_data, submit


def mask_num(mask, num, bits=36):
    num = "{0:b}".format(num).zfill(bits)
    out = []
    for m, n in zip(mask, num):
        if m != "X":
            out.append(m)
        else:
            out.append(n)
    return int("".join(out), 2)


def find_a(lines):
    mask = None
    mem = defaultdict(int)
    for line in lines:
        instr, data = line.split(" = ")
        if instr == "mask":
            mask = data
        elif "mem" in instr:
            addr = int(instr.split("[")[1].strip("]"))
            num = mask_num(mask, int(data))
            mem[addr] = num
    return sum(mem.values())


def fill_x(mask, replacements):
    mask = list(mask)
    for repl in replacements:
        i = mask.index("X")
        mask[i] = str(repl)
    return "".join(mask)


def gen_addrs(mask, addr, bits=36):
    num = "{0:b}".format(addr).zfill(bits)
    out = []
    for m, n in zip(mask, num):
        if m in ("X", "1"):
            out.append(m)
        else:
            out.append(n)
    base_addr = "".join(out)
    xes = base_addr.count("X")
    replacements = product(*[[0, 1] for _ in range(xes)])
    for repl in replacements:
        yield int(fill_x(base_addr, repl), 2)


def find_b(lines):
    mask = None
    mem = defaultdict(int)
    for line in lines:
        instr, data = line.split(" = ")
        if instr == "mask":
            mask = data
        elif "mem" in instr:
            addr = int(instr.split("[")[1].strip("]"))
            for masked_addr in gen_addrs(mask, addr):
                mem[masked_addr] = int(data)
    return sum(mem.values())


if __name__ == "__main__":
    d = get_data()
    lines = [line for line in d.split("\n") if line]
    answer_a = find_a(lines)
    submit(answer_a, part="a", day=14, year=2020)

    answer_b = find_b(lines)
    submit(answer_b, part="b", day=14, year=2020)
