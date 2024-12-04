import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view as swv
from io import StringIO

def get_input(filepath: str) -> str:
    """Grabs the entire contents of a text file"""
    with open(filepath, 'r') as f:
        return f.read()

def wordsearch(grid: str, n: int) -> tuple[list[str]]:
    r"""
    For a given word length `n`, applies a rolling window over the grid.
    Extracts all distinct spans of `n` consecutive characters,
    including horizontal, vertical, and diagonal.
    Does not double count.
    
    returns:
        Lists of spans: — | \ /
    """
    arr = pd.DataFrame([list(r) for r in grid.split('\n')]).to_numpy()
    horiz = swv(arr, (1, n)).reshape(-1,n)
    vert = swv(arr, (n, 1)).reshape(-1, n)
    diags = swv(arr, (n, n)).reshape(-1, n, n)
    ltr = [a.diagonal() for a in diags]
    rtl = [a[::-1].diagonal() for a in diags]
    
    return horiz, vert, ltr, rtl

# Part 1:

def count(grid: str, word: str) -> int:
    count = 0
    for axis in wordsearch(grid, len(word)):
        for arr in axis:
            if ''.join(arr) in (word, word[::-1]):
                count += 1
    return count


# Part 2:

def count_x(grid: str, word: str) -> int:
    _, _, ltr, rtl = wordsearch(grid, len(word))
    count = 0
    targets = (word, word[::-1])
    for a, b in zip(ltr, rtl):
        if ''.join(a) in targets and ''.join(b) in targets:
            count += 1
    return count


# Tests:

given_test = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""


def test_part1():
    assert count(given_test, "XMAS") == 18


def test_part2():
    assert count_x(given_test, "MAS") == 9