from aocd import get_data, submit

MOVES = {"N": 1j, "S": -1j, "E": 1, "W": -1}
ROTATIONS = {"L": 0 + 1j, "R": 0 - 1j}


class Ferry:
    def __init__(self, instructions):
        self.instructions = instructions
        self.position = 0 + 0j
        self.heading = 1 + 0j
        self.letter = None
        self.amount = None

    def parse_instruction(self, instruction):
        self.letter = instruction[0]
        self.amount = int(instruction[1:])

    def rotate(self):
        for _ in range(int(self.amount / 90)):
            self.heading *= ROTATIONS[self.letter]

    def translate(self):
        self.position += self.amount * MOVES[self.letter]

    def forward(self):
        self.position += self.amount * self.heading

    def follow_instructions(self):
        for instruction in self.instructions:
            self.parse_instruction(instruction)
            if self.letter in "LR":
                self.rotate()
            elif self.letter in "NSEW":
                self.translate()
            else:
                self.forward()

    def calc_distance_from_start(self):
        return int(abs(self.position.imag) + abs(self.position.real))


class Waypoint(Ferry):
    def __init__(self, instructions):
        super().__init__(instructions)
        self.position = 10 + 1j
        self.ferry = Ferry([])

    def rotate(self):
        for _ in range(int(self.amount / 90)):
            self.position *= ROTATIONS[self.letter]

    def forward(self):
        self.ferry.amount = self.amount
        self.ferry.heading = self.position
        self.ferry.forward()


if __name__ == "__main__":
    d = get_data()
    inputs = [line for line in d.split("\n") if line]

    f = Ferry(inputs)
    f.follow_instructions()
    answer_a = f.calc_distance_from_start()
    submit(answer_a, part="a", day=12, year=2020)

    w = Waypoint(inputs)
    w.follow_instructions()
    answer_b = w.ferry.calc_distance_from_start()
    submit(answer_b, part="b", day=12, year=2020)
