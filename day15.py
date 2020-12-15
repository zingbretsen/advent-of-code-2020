from aocd import get_data, submit


def find_nth_num(nums, n):
    nums = nums[:]
    new_num = nums.pop()

    num_dict = dict()
    for i, num in enumerate(nums):
        num_dict[num] = i

    for i in range(len(nums), n):
        idx = num_dict.get(new_num, i)
        num_dict[new_num] = i
        prev_num, new_num = new_num, i - idx

    return prev_num


if __name__ == "__main__":
    d = get_data()
    nums = [int(num) for num in d.split(",") if num]

    answer_a = find_nth_num(nums, 2020)
    submit(answer_a, part="a", day=15, year=2020)

    answer_b = find_nth_num(nums, 30000000)
    submit(answer_b, part="b", day=15, year=2020)
