#! /usr/bin/env python

from utils import AOCrunner, Posn2D, Window

INPUTFILE = r"inputs/day4.txt"

TESTCASE = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

type Matrix = list[list[str]]


def parse(f) -> Matrix:
    """
    Convert the input into a 2d matrix.
    Replace rolls with 1, and other slots with 0,
    so that we can use math to count rolls.
    """
    mat = []
    for line in f:
        mat.append([])
        for symbol in line.strip():
            mat[-1].append(1 if symbol == "@" else 0)
    return mat


def find_accessible(mat: Matrix) -> list[Posn2D]:
    """
    Compute a sliding window over the matrix, centered on each slot.
    Because the shape of the window will change around the edges of the grid,
    we need the `divmod(i, len(mat[0]))` to find the center.

    For part 1 we just need to count the rolls,
    but for part 2 we need to know where they are.
    Thus, we'll return a list of the coordinates of each roll.
    """
    rolls = []
    for i, window in enumerate(Window.slide_centered(mat, (3, 3))):
        row, col = divmod(i, len(mat[0]))
        if mat[row][col]:
            if sum(sum(row) for row in window) < 5:
                rolls.append(Posn2D(row, col))

    return rolls


def remove_rolls(mat: Matrix) -> int:
    """
    Recursively count the accessible rolls and remove them.
    """
    rolls = find_accessible(mat)
    if not rolls:
        return 0

    for pos in rolls:
        mat[pos.x][pos.y] = 0
    return len(rolls) + remove_rolls(mat)


def count_accessible_rolls(f) -> int:
    return len(find_accessible(parse(f)))


def count_removed_rolls(f) -> int:
    return remove_rolls(parse(f))


if __name__ == "__main__":
    aoc = AOCrunner(INPUTFILE, TESTCASE)
    aoc.part1(count_accessible_rolls, 13)
    aoc.part2(count_removed_rolls, 43)
