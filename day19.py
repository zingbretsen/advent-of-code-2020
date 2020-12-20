from aocd import get_data, submit
from string import ascii_lowercase
from itertools import product


def derive_rules(rules):
    rule_dict = dict()
    for rule in rules.split("\n"):
        key, value = rule.split(": ")
        key = int(key)
        value = value.strip('"')
        if not all(v in ascii_lowercase for v in value):
            values = value.split(" | ")
            value = [list(map(int, v.split())) for v in values]
        rule_dict[key] = value
    return rule_dict


def find_all_matches(rule_dict, n=0):
    value = rule_dict[n]
    if type(value) is str:
        return [value]
    else:
        out_list = []
        for option in value:
            out = []
            for v in option:
                o = find_all_matches(rule_dict, v)
                out.append(o)
            out = ["".join(p) for p in product(*out)]
            out_list.extend(out)
        return out_list


def count_matches(messages, all_matches):
    c = 0
    invalid_messages = set()
    for message in messages:
        if message in all_matches:
            c += 1
        else:
            invalid_messages.add(message)
    return c, invalid_messages


def count_expanded_matches(invalid_messages):
    # Part B must start with one or more 42 and end with one or more 31
    # The number of 31s must be at most the number of 42s minus one
    forty_two = find_all_matches(rule_dict, 42)
    thirty_one = find_all_matches(rule_dict, 31)

    # Fortunately, all of the patterns are 8 chars long
    l1 = len(forty_two[0])
    l2 = len(thirty_one[0])

    c = 0
    for vm in invalid_messages:
        a = b = 0
        # Find all strings that match any of the patterns from rule 31
        # at the end of the string
        while len(vm) > 0 and vm[-l2:] in thirty_one:
            b += 1
            vm = vm[:-l2]
        # There should be at least 1
        if b > 0:
            # Find all strings that match any of the patterns from rule 42
            # at the beginning of the string
            while vm != "" and vm[:l1] in forty_two:
                a += 1
                vm = vm[l1:]

        # There should be at least one more 42 than 31
        # If the string is entirely composed of 42s and 31s, it is a match
        if a > b > 0 and vm == "":
            c += 1
    return c


if __name__ == "__main__":
    rules, messages = get_data().split("\n\n")
    messages = messages.split("\n")

    rule_dict = derive_rules(rules)
    all_matches = set(find_all_matches(rule_dict, n=0))

    c, invalid_messages = count_matches(messages, all_matches)
    print(c)
    submit(c, part="a", day=19, year=2020)

    c += count_expanded_matches(invalid_messages)
    print(c)
    submit(c, part="b", day=19, year=2020)
