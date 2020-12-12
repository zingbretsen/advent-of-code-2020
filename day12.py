from aocd import get_data, submit


class Ferry:
    def __init__(self, instructions):
        self.instructions = instructions
        self.position = complex(0, 0)
        self.heading = complex(1, 0)
        self.letter = None
        self.amount = None

    def parse_instruction(self, instruction):
        self.letter = instruction[0]
        self.amount = int(instruction[1:])

    def rotate(self):
        if self.letter == "L":
            self.letter = "R"
            self.amount = (360 - self.amount) % 360
        while self.amount > 0:
            self.heading *= complex(0, -1)
            self.amount -= 90

    def translate(self):
        if self.letter in "SW":
            sign = -1
        else:
            sign = 1
        if self.letter in "NS":
            heading = sign * complex(0, 1)
        else:
            heading = sign * complex(1, 0)

        self.position += self.amount * heading

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


class Waypoint:
    def __init__(self, instructions):
        self.instructions = instructions
        self.position = complex(10, 1)
        self.rotation = complex(0, 0)
        self.letter = None
        self.amount = None
        self.ferry = Ferry([])

    def parse_instruction(self, instruction):
        self.letter = instruction[0]
        self.amount = int(instruction[1:])

    def rotate(self):
        if self.letter == "L":
            self.letter = "R"
            self.amount = (360 - self.amount) % 360
        while self.amount > 0:
            self.position *= complex(0, -1)
            self.amount -= 90

    def translate(self):
        if self.letter in "SW":
            sign = -1
        else:
            sign = 1
        if self.letter in "NS":
            rotation = sign * complex(0, 1)
        else:
            rotation = sign * complex(1, 0)

        self.position += self.amount * rotation

    def forward(self):
        self.ferry.amount = self.amount
        self.ferry.heading = self.position
        self.ferry.forward()

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
        return self.ferry.calc_distance_from_start()


if __name__ == "__main__":
    d = get_data()
    inputs = [line for line in d.split("\n") if line]
    f = Ferry(inputs)
    f.follow_instructions()
    answer_a = f.calc_distance_from_start()
    submit(answer_a, part="a", day=12, year=2020)

    w = Waypoint(inputs)
    w.follow_instructions()
    answer_b = w.calc_distance_from_start()
    submit(answer_b, part="b", day=12, year=2020)
