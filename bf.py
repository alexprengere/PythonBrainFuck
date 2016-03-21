#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Brainfuck interpreter.
"""

#pylint: disable=pointless-statement
from __future__ import with_statement, print_function
from sys import argv, stdin, stdout


def create_jump_table(chars):
    jump_table = {}
    left_positions = []

    position = 0
    for char in chars:
        if char == '[':
            left_positions.append(position)

        elif char == ']':
            left = left_positions.pop()
            right = position
            jump_table[left] = right
            jump_table[right] = left
        position += 1

    return jump_table


class Cells(object):
    def __init__(self):
        self.cells = [0]
        self.index = 0

    def get(self):
        return self.cells[self.index]

    def set(self, n):
        self.cells[self.index] = n

    def __iadd__(self, n): # +=
        self.cells[self.index] += n
        return self

    def __isub__(self, n): # -=
        self.cells[self.index] -= n
        if self.cells[self.index] < 0:
            self.cells = 0
        return self

    def __lshift__(self, n): # <<
        self.index -= n
        if self.index < 0:
            self.index = 0

    def __rshift__(self, n): # >>
        for _ in range(n):
            self.index += 1
            if self.index >= len(self.cells):
                self.cells.append(0)


def run(chars):
    """Actual BrainFuck Interpreter."""
    jump_table = create_jump_table(chars)
    cells = Cells()

    position = 0
    while position < len(chars):
        char = chars[position]

        if char == '>':
            cells >> 1

        elif char == '<':
            cells << 1

        elif char == '+':
            cells += 1

        elif char == '-':
            cells -= 1

        elif char == '.':
            stdout.write(chr(cells.get() % 256))

        elif char == ',':
            cells.set(ord(stdin.read(1)))

        elif char == '[' and cells.get() == 0:
            position = jump_table[position]

        elif char == ']' and cells.get() != 0:
            position = jump_table[position]

        position += 1


if __name__ == '__main__':

    if len(argv) == 1 and stdin.isatty():
        print('Usage: {0} file'.format(argv[0]))
        print('Usage: cat file | {0}'.format(argv[0]))
        exit(1)

    if not stdin.isatty():
        chars = ''.join(row for row in stdin)
    else:
        with open(argv[1]) as f:
            chars = f.read()

    codes = set('<>[]-+,.')
    run(''.join(c for c in chars if c in codes))
