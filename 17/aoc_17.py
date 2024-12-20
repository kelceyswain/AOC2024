#! /usr/bin/env python3
import re


class Computer:
    def __init__(self, program: str, a: int = 0, b: int = 0, c: int = 0):
        self.A = a
        self.B = b
        self.C = c
        self.pointer = 0
        self.program = [int(p.strip()) for p in program.split(',')]
        self._output = []

    def debug(self):
        print(f"A={self.A}, B={self.B}, C={self.C}, pointer={self.pointer}, output={self._output}")

    @property
    def output(self):
        return ",".join([str(t) for t in self._output])

    def run(self):
        while self.pointer < (len(self.program) - 1):
            opcode = self.program[self.pointer]
            operand = self.program[self.pointer+1]
            self.operate(opcode, operand)

    def operate(self, opcode, operand):
        combo = operand
        if combo == 4:
            combo = self.A
        elif combo == 5:
            combo = self.B
        elif combo == 6:
            combo = self.C

        if opcode == 0:
            # adv
            div = int(self.A / (2**combo))
            self.A = div
            self.pointer += 2
        elif opcode == 1:
            # bxl
            self.B = self.B ^ operand
            self.pointer += 2
        elif opcode == 2:
            # bst
            self.B = combo % 8
            self.pointer += 2
        elif opcode == 3:
            if self.A == 0:
                self.pointer += 2
            else:
                self.pointer = operand
        elif opcode == 4:
            self.B = self.B ^ self.C
            self.pointer += 2
        elif opcode == 5:
            self._output.append(combo % 8)
            self.pointer += 2
        elif opcode == 6:
            div = int(self.A / (2**combo))
            self.B = div
            self.pointer += 2
        elif opcode == 7:
            div = int(self.A / (2**combo))
            self.C = div
            self.pointer += 2
        # self.debug()


if __name__ == "__main__":
    with open("test.txt") as puzzle_file:
        puzzle_input = puzzle_file.read()
    pat_reg = re.compile(r"Register [ABC]: (\d+)")
    pat_prog = re.compile(r"Program: (.*)")
    reg_A, reg_B, reg_C = [int(r) for r in pat_reg.findall(puzzle_input)]
    program = pat_prog.findall(puzzle_input)[0]
    c = Computer(program, reg_A, reg_B, reg_C)
    c.run()
    print(f"Part 1: {c.output}")
