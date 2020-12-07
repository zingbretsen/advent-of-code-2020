import re
from collections import defaultdict
from aocd import get_data, submit


def parse_line(line, contained_dict, container_dict):
    if re.match(".*no other bags.*", line) is not None:
        return dict()
    container, bags = line.strip(".").split(" bags contain ")
    bags = bags.split(", ")
    for bag in bags:
        matches = re.match("([0-9]+) (.+) bags?", bag)
        count = int(matches.group(1))
        bag = matches.group(2)
        contained_dict[bag].add(container)
        container_dict[container].append({"type": bag, "count": count})


def find_containers(contained_dict, starting_bag="shiny gold"):
    checked = set()
    frontier = contained_dict[starting_bag]
    while len(frontier) != 0:
        bag = frontier.pop()
        checked.add(bag)
        for new_container in contained_dict[bag]:
            if new_container not in checked:
                frontier.add(new_container)
    return checked


def count_contained(bags, starting_bag="shiny gold", n_bags=1):
    print(starting_bag, n_bags)
    c = 0
    for bag in bags[starting_bag]:
        next_bag = bag["type"]
        count = bag["count"]
        c += n_bags * count
        c += count_contained(bags, next_bag, count) * n_bags
    return c


if __name__ == "__main__":
    d = get_data()

    contained_dict = defaultdict(set)
    container_dict = defaultdict(list)
    count_dict = defaultdict(int)

    for line in d.split("\n"):
        parse_line(line, contained_dict, container_dict)

    answer_a = len(find_containers(contained_dict))
    submit(answer_a, part="a", day=7, year=2020)

    answer_b = count_contained(container_dict)
    submit(answer_b, part="b", day=7, year=2020)
