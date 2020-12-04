# a: 237
# b: 172
import re

from aocd import get_data, submit


def parse_lines(lines):
    line = " ".join(lines.split("\n"))
    items = (item.split(":") for item in line.split(" "))
    return {k: v for k, v in items}


def valid_a(items, keys={"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}):
    return all(key in items.keys() for key in keys)


def valid_byr(byr):
    return 1920 <= int(byr) <= 2002


def valid_iyr(iyr):
    return 2010 <= int(iyr) <= 2020


def valid_eyr(eyr):
    return 2020 <= int(eyr) <= 2030


def valid_hgt(hgt):
    if len(hgt) < 3:
        return False
    num, unit = hgt[:-2], hgt[-2:]
    num = int(num)
    if unit == "cm":
        return 150 <= num <= 193
    elif unit == "in":
        return 59 <= num <= 76
    return False


def valid_hcl(hcl):
    return re.match(string=hcl, pattern="#[0-9a-f]{6}")


def valid_ecl(ecl):
    return ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def valid_pid(pid):
    return re.match(string=pid, pattern="^[0-9]{9}$")


def valid_b(byr, iyr, eyr, hgt, hcl, ecl, pid, **kwargs):
    return all(
        (
            valid_byr(byr),
            valid_iyr(iyr),
            valid_eyr(eyr),
            valid_hgt(hgt),
            valid_hcl(hcl),
            valid_ecl(ecl),
            valid_pid(pid),
        )
    )


if __name__ == "__main__":
    d = get_data()
    inputs = [parse_lines(lines) for lines in d.split("\n\n")]

    answer_a = sum(valid_a(line) for line in inputs)
    submit(answer_a, part="a", day=4, year=2020)

    answer_b = sum(valid_b(**line) for line in inputs if valid_a(line))
    print(answer_b)
    submit(answer_b, part="b", day=4, year=2020)
