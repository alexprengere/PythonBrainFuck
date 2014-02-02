#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Brainfuck interpreter.
"""

from __future__ import with_statement
from sys import argv, stdin, stdout

# Cells and pointer
IND   = 0
CELLS = []


def every_char_from(flow):
    """Yields every char from flow.
    """
    for row in flow:
        for char in row:
            yield char


def get_char():
    """Quick and dirty getchar implementation.
    """
    try:
        return raw_input()[0]
    except EOFError:
        return '0'


def init():
    """We have lazy cell creation with this.
    """
    if len(CELLS) - 1 < IND:
        CELLS.append(0)


def nested(chars):
    """Looking for the next same-level ']'.
    """
    i = 0

    while chars[0:i+1].count("[") != chars[0:i+1].count("]"):
        i += 1

    return chars[1:i]



def run(chars):
    """Run a sequence of chars.
    """
    global IND

    init()
    position = 0

    while position < len(chars):
        char = chars[position]

        if char == '>':
            IND += 1
            init() # if it is a not-yet-visited cell, we put a 0

        elif char == '<':
            if IND: # IND is always >= 0
                IND -= 1

        elif char == '+':
            CELLS[IND] += 1

        elif char == '-':
            if CELLS[IND]: # values are >= 0
                CELLS[IND] -= 1

        elif char == '.':
            stdout.write(chr(CELLS[IND] % 256))

        elif char == ',':
            CELLS[IND] = ord(get_char())

        elif char == '[':
            nest = nested(chars[position:])

            while CELLS[IND]:
                run(nest)

            position += len(nest) + 1

        position += 1


if __name__ == '__main__':

    if not stdin.isatty():
        run(list(every_char_from(stdin)))

    elif len(argv) > 1:
        with open(argv[1]) as f:
            run(list(every_char_from(f)))

    else:
        print 'Usage: %s file' % argv[0]
        print 'Usage: cat file | %s' % argv[0]

