import pandas as pd
import numpy as np
from io import StringIO

"""
I spent an embarrasingly long time on this one by counting the valid cases instead of summing them.
Reading the prompt explains the prompt. -_-
"""


def get_input(src:str) -> pd.DataFrame:
    """
    Nudges the input into a DF.
    If `src` is a text file name, loads it using Pandas. 
    15 columns should be enough not to crash on load, and labels aren't used for the logic anyway.
    If `src` is any other string, loads its contents into the DF.
    """
    if not src.endswith('.txt'):
        src = StringIO(src)
    return pd.read_csv(src, sep=r':? ', header=None, engine='python', names=range(15))


def deconcat(target: int, val: int) -> int:
    """
    Performs the inverse of `target || val`.
    (e.g. `deconcat(1234, 34)` => `12`)
    Assumes that `target` ends with `val`.
    If `target` and `val` are the same length, returns 0.
    """
    cut = str(target)[:-len(str(val))]
    if cut == '':
        return 0
    else:
        return int(cut)

def sat(target: int, vals: tuple[int], concat=True) -> bool:
    """
    Check if an equation of the form 
        `target = vals_1 {o in ops} vals_2 ...`
    is satisfiable under ops {+ *}. No operator precedence is applied.

    Recursively reverse-engineers a valid solution, noting that:
        t = a * b + c * d ...
    is the same as
        t = ... (d * (c + (b * a))).
    This is why `sum_sat` reverses `vals`.

    params:
        target: The LHS.
        vals: The values on the RHS.
        concat: Include `||` as an operator.
    """
    x = vals[0]
    if len(vals) == 2:
        y = vals[1]
        if concat:
            return target in (y * x, y + x, int(f'{y}{x}'))
        else:
            return target in (y * x, y + x)
    else:
        rest = vals[1:]
        
        # Backtrack 1: (...) + x
        sub = sat(target - x, rest, concat=concat)
        
        # Backtrack 2: (...) * x
        # (Skip if `target` isn't divisible by x.)
        div = sat(int(target / x), rest, concat=concat) if target % x == 0 else False
        
        # Backtrack 3: (...) || x
        # (Skip if `target` doesn't end with x.)
        deconc = sat(deconcat(target, x), rest, concat=concat) if str(target).endswith(str(x)) else False
        
        return sub or div or (deconc and concat)


def filter_na(vals: tuple[int]) -> tuple[int]:
    """Removes NaNs from a tuple. No mutation."""
    return tuple([int(v) for v in vals if not np.isnan(v)])


def sum_sat(src:str, concat=True, verbose=False):
    """
    Solves both parts of Day 7, by counting the sums of satisfiable equations.

    params:
        src: The input source.
        concat: See `sat`.
        verbose: Print all satisfiable equations.
    """
    df = get_input(src)
    total = 0
    for t in df.itertuples(index=False):
        target = t[0]
        vals = filter_na(t[-1:0:-1]) # Reverse all items exlcuding the first
        if sat(target, vals, concat=concat):
            if verbose:
                print(target, vals)
            total += target
    return total


# Tests

given = \
"""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

# Part 1
def test_part1():
    print(sum_sat(given, concat=False))
    assert sum_sat(given, concat=False) == 3749

# Part 2
def test_part2():
    assert sum_sat(given, concat=True) == 11387
    