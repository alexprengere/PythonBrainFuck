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


def run(chars):
    """Actual BrainFuck Interpreter."""
    jump_table = create_jump_table(chars)
    cells = [0] * 10000
    index = 0

    position = 0
    while position < len(chars):
        char = chars[position]

        if char == '>':
            index += 1

        elif char == '<':
            if index > 0:
                index -= 1

        elif char == '+':
            cells[index] += 1

        elif char == '-':
            if cells[index] > 0:
                cells[index] -= 1

        elif char == '.':
            sys.stdout.write(chr(cells[index] % 256))
            sys.stdout.flush()

        elif char == ',':
            cells[index] = ord(raw_input())

        elif char == '[' and cells[index] == 0:
            position = jump_table[position]

        elif char == ']' and cells[index] != 0:
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
