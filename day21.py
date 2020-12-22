import math
import numpy as np

from copy import deepcopy
from aocd import get_data, submit

from collections import defaultdict
import re


def parse_ingredients(recipe):
    recipe = recipe.replace(",", "")

    allergens = re.match(string=recipe, pattern=r"(.*) \(contains (.*)\)")
    ingredients = allergens.group(1).split()
    allergens = allergens.group(2).split()

    return ingredients, allergens


if __name__ == "__main__":
    dd = get_data()

    dd = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

    data = [parse_ingredients(d) for d in dd.split("\n")]
    print([len(d[0]) for d in data])
    forward_index = defaultdict(set)
    backward_index = defaultdict(set)

    all_ingredients = set()
    all_allergens = set()

    for d in data:
        for ingredient in d[0]:
            for allergen in d[1]:
                forward_index[ingredient].add(allergen)
                backward_index[allergen].add(ingredient)

                all_ingredients.add(ingredient)
                all_allergens.add(allergen)

    allergen_dict = dict()
    for k, v in backward_index.items():
        for ingredients, allergens in data:
            if k in allergens:
                backward_index[k] = set(ingredients) & backward_index[k]

    final_dict = dict()
    lengths = {k: len(v) for k, v in backward_index.items() if len(v) > 0}
    for k, v in lengths.items():
        if v == 1:
            value = backward_index[k].pop()
            final_dict[k] = value
            for kk, vv in backward_index.items():
                if value in vv:
                    vv.remove(value)

    safe_ingredients = []
    for ingredients, allergens in data:
        for ingredient in ingredients:
            if ingredient not in final_dict.values():
                safe_ingredients.append(ingredient)

    answer_a = len(safe_ingredients)
    print(answer_a)

    submit(answer_a, part="a", day=21, year=2020)

    sorted_allergens = sorted((k, v) for k, v in final_dict.items())
    answer_b = ",".join(a[1] for a in sorted_allergens)
    print(answer_b)
    submit(answer_b, part="b", day=21, year=2020)
