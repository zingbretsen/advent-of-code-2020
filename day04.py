# a: 237
# b: 172
import re

from aocd import get_data, submit

def parse_lines(lines):
    line = ' '.join(lines.split('\n'))
    items = (item.split(':') for item in line.split(" "))
    return {k: v for k, v in items}


def valid_a(items, keys = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}):
    return all(key in items.keys() for key in keys)

def valid_byr(byr):
    byr = int(byr)
    if byr < 1920 or byr > 2002:
        return False
    return True

def valid_iyr(iyr):
    iyr = int(iyr)
    if iyr < 2010 or iyr > 2020:
        return False
    return True

def valid_eyr(eyr):
    eyr = int(eyr)
    if eyr < 2020 or eyr > 2030:
        return False
    return True

def valid_hgt(hgt):
    if len(hgt) < 3:
        return False
    num, unit = hgt[:-2], hgt[-2:]
    num = int(num)
    if unit == 'cm':
        if num < 150 or num > 193:
            return False
    elif unit == 'in':
        if num < 59 or num > 76:
            return False
    else:
        return False
    return True

def valid_hcl(hcl):
    if re.match(string=hcl, pattern='#[0-9a-f]{6}'):
        return True
    return False

def valid_ecl(ecl):
    return ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def valid_pid(pid):
    if re.match(string=pid, pattern='^[0-9]{9}$'):
        return True
    return False

def valid_b(byr, iyr, eyr, hgt, hcl, ecl, pid, **kwargs):
    return all((valid_byr(byr),
                valid_iyr(iyr),
                valid_eyr(eyr),
                valid_hgt(hgt),
                valid_hcl(hcl),
                valid_ecl(ecl),
                valid_pid(pid)))

if __name__ == '__main__':
    d = get_data()
    inputs = [parse_lines(lines) for lines in d.split('\n\n')]

    answer_a = sum(valid_a(line) for line in inputs)
    submit(answer_a, part='a', day=4, year=2020)

    answer_b = sum(valid_b(**line) for line in inputs if valid_a(line))
    submit(answer_b, part='b', day=4, year=2020)
