#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Brainfuck interpreter.
"""

import sys
import os


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

    def increment(self):
        self.cells[self.index] += 1

    def decrement(self):
        if self.cells[self.index] > 0:
            self.cells[self.index] -= 1

    def left(self):
        if self.index > 0:
            self.index -= 1

    def right(self):
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
            cells.right()

        elif char == '<':
            cells.left()

        elif char == '+':
            cells.increment()

        elif char == '-':
            cells.decrement()

        elif char == '.':
            os.write(1, chr(cells.get() % 256))

        elif char == ',':
            cells.set(ord(os.read(0, 1)[0]))

        elif char == '[' and cells.get() == 0:
            position = jump_table[position]

        elif char == ']' and cells.get() != 0:
            position = jump_table[position]

        position += 1


def remove_comments(chars):
    codes = '<>[]-+,.'
    tmp = ""
    for c in chars:
        if c in codes:
            tmp += c
    return tmp


def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "Usage: %s program.bf" % argv[0]
        return 1

    fp = os.open(filename, os.O_RDONLY, 0777)
    chars = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        chars += read
    os.close(fp)

    run(remove_comments(chars))
    return 0


def target(*args):
    #pylint: disable=unused-argument
    return entry_point, None


if __name__ == "__main__":
    entry_point(sys.argv)
