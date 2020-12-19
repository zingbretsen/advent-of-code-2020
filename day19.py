import re
from string import ascii_lowercase
from operator import add, mul

from aocd import get_data, submit


def find_all_matches(rules, n="0"):
    rule = rules[n]
    all_rules = []
    while rule not in ascii_lowercase:
        for n in rule:
            find_all_matches(rules, n)
    return all_rules


from itertools import product


def x(rules, n=1):
    value = rules[n]
    print("XXX", n, value)
    if type(value) is str:
        return [value]
    else:
        out_list = []
        for option in value:
            out = []
            for v in option:
                o = x(rules, v)
                out.append(o)
            print("out: ", out)
            breakpoint()
            out_list.append(list(product(*out)))
        print("out_list: ", out_list)
        return out_list
        # return list(product(*out_list))


print(x(rule_dict, 2))

if __name__ == "__main__":
    rules, messages = get_data().split("\n\n")
    rules = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"'''

    rules = '''0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"'''
    rule_dict = dict()
    for rule in rules.split("\n"):
        key, value = rule.split(": ")
        key = int(key)
        value = value.strip('"')
        if not all(v in ascii_lowercase for v in value):
            values = value.split(" | ")
            value = [list(map(int, v.split())) for v in values]
        rule_dict[key] = value

    rules = {rule.split(": ")[0]: rule.split(": ")[1].split()}
    all_matches = find_all_matches(rules)

    answer_a = sum(parse_equation(e) for e in lines)
    submit(answer_a, part="a", day=18, year=2020)

    answer_b = sum(parse_equation_advanced(e) for e in lines)
    submit(answer_b, part="b", day=18, year=2020)
