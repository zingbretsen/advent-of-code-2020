from collections import Counter
from aocd import get_data, submit


def parse_line(line):
    nums, letter, password = line.split()
    mn, mx = [int(num) for num in nums.split('-')]
    letter = letter.strip(":")
    return mn, mx, letter, password

def valid_a(mn, mx, letter, password):
    password = Counter(password)
    return mn <= password[letter] <= mx

def valid_b(pos_a, pos_b, letter, password):
    return (password[pos_a - 1] == letter) ^ (password[pos_b - 1] == letter)

if __name__ == '__main__':
    d = get_data(day=2, year=2020)
    inputs = [parse_line(line) for line in d.split('\n')]

    n_good_passwords_a = sum(valid_a(*input) for input in inputs)
    submit(n_good_passwords_a, part='a', day=2, year=2020)

    n_good_passwords_b = sum(valid_b(*input) for input in inputs)
    submit(n_good_passwords_b, part='b', day=2, year=2020)
