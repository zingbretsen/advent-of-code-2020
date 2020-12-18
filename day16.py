import math
from aocd import get_data, submit


def parse_rules(rules):
    rules = rules.split("\n")
    rule_dict = dict()
    for rule in rules:
        name, nums = rule.split(": ")
        nums = [[int(n) for n in num.split("-")] for num in nums.split(" or ")]
        rule_dict[name] = nums
    return rule_dict


def all_valid_numbers(rules):
    all_valid = set()
    for values in rules.values():
        for rule in values:
            for num in range(rule[0], rule[1] + 1):
                all_valid.add(num)
    return all_valid


def find_invalid_numbers(ticket, all_valid):
    return not all(t in all_valid for t in ticket)


def find_possible_categories(rules, column):
    possible_cats = set()
    for k, v in rules.items():
        good_cat = True
        values = set()
        for val in v:
            for i in range(val[0], val[1] + 1):
                values.add(i)
            values.add(val[-1])
        for c in column:
            if c not in values:
                good_cat = False
                break
        if good_cat:
            possible_cats.add(k)
    return possible_cats


def get_col(tickets, n):
    return [ticket[n] for ticket in tickets]


def get_cols(tickets):
    l = len(tickets[0])
    return [get_col(tickets, i) for i in range(l)]


def get_cats(rules, cols):
    return [find_possible_categories(rules, col) for col in cols]


def assign_cats(cats):
    final_cats = dict()
    while True:
        n_cats = [len(cat) for cat in cats]
        try:
            single_cat_idx = n_cats.index(1)
        except ValueError:
            return final_cats
        single_cat = cats[single_cat_idx].pop()
        final_cats[single_cat_idx] = single_cat
        for cat in cats:
            try:
                cat.remove(single_cat)
            except KeyError:
                pass


import pandas as pd

if __name__ == "__main__":
    d = get_data(day=16)

    d = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""

    rules, my_ticket, tickets = d.split("\n\n")
    rules = parse_rules(rules)
    my_ticket = [int(x) for x in my_ticket.split("\n")[1].split(",")]
    tickets = [
        [int(t) for t in ticket.split(",")] for ticket in tickets.split("\n")[1:]
    ]

    all_valid = all_valid_numbers(rules)
    answer_a = sum(find_invalid_numbers(ticket, all_valid) for ticket in tickets)
    submit(answer_a, part="a", day=16, year=2020)

    valid_tickets = [t for t in tickets if find_invalid_numbers(t, all_valid) == 0]

    cols = get_cols(valid_tickets)
    cats = get_cats(rules, cols)
    final_cats = assign_cats(cats)
    final_idx = [k for k, v in final_cats.items() if "departure" in v]

    answer_b = math.prod(my_ticket[i] for i in final_idx)
    submit(answer_b, part="b", day=16, year=2020)
