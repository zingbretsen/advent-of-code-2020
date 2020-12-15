from itertools import product
from collections import deque
from aocd import get_data, submit


def find_nth_num(nums, n):
    nums = nums[:]
    new_num = nums.pop()

    num_dict = dict()
    for i, num in enumerate(nums):
        num_dict[num] = i

    for i in range(len(nums), n):
        num_dict[new_num], idx = i, num_dict.get(new_num, i)
        # = i
        prev_num, new_num = new_num, i - idx

    return prev_num


if __name__ == "__main__":
    d = get_data()
    nums = [int(num) for num in d.split(",") if num]

    # answer_a: 289
    answer_a = find_nth_num(nums, 2020)
    assert answer_a == 289, "Wrong A"
    submit(answer_a, part="a", day=15, year=2020)

    # answer_b: 1505722
    answer_b = find_nth_num(nums, 30000000)
    assert answer_b == 1505722, "Wrong B"
    submit(answer_b, part="b", day=15, year=2020)
