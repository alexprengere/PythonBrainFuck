#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


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


class Array(object):
    def __init__(self):
        self._cells = [0] * 10000  # preallocation
        self._index = 0

    def get(self):
        return self._cells[self._index]

    def set(self, n):
        self._cells[self._index] = n

    def increment(self):
        self._cells[self._index] += 1

    def decrement(self):
        if self._cells[self._index] > 0:
            self._cells[self._index] -= 1

    def right(self):
        self._index += 1
        if self._index >= len(self._cells):
            self._cells.append(0)

    def left(self):
        if self._index > 0:
            self._index -= 1


def run(chars):
    """Actual BrainFuck Interpreter."""
    jump_table = create_jump_table(chars)
    ptr = Array()

    position = 0
    while position < len(chars):
        char = chars[position]

        if char == '>':
            ptr.right()

        elif char == '<':
            ptr.left()

        elif char == '+':
            ptr.increment()

        elif char == '-':
            ptr.decrement()

        elif char == '.':
            sys.stdout.write(chr(ptr.get() % 256))
            sys.stdout.flush()

        elif char == ',':
            ptr.set(ord(raw_input()))

        elif char == '[' and ptr.get() == 0:
            position = jump_table[position]

        elif char == ']' and ptr.get() != 0:
            position = jump_table[position]

        position += 1


def remove_comments(chars):
    codes = '<>[]-+,.'
    tmp = ""
    for c in chars:
        if c in codes:
            tmp += c
    return tmp


if __name__ == "__main__":
    run(remove_comments(open(sys.argv[1]).read()))
