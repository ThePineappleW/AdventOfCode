from io import StringIO
from sympy import Matrix, solve_linear_system
from sympy.abc import a, b

from itertools import batched
from re import findall

"""
SymPy go brrrr...
"""

def parse_nums(s) -> list[int]:
    """Extracts numbers from a string."""
    return [int(n) for n in findall(r'\d+', s)]


def parse(src:str) -> tuple[list[int]]:
    """Yields a triple of x-y pairs of values for the A button, B button, and Target."""
    if src.endswith('.txt'):
        with open(src, 'r') as f:
            lines = f.readlines()
            lines.append('') # Do this to make sure all machines are exactly 4 lines.
    else:
        lines = src.split('\n')
        
    for button_a, button_b, target, _ in batched(lines, 4):
        yield parse_nums(button_a), parse_nums(button_b), parse_nums(target)


def solve_machine(src:str, buffer=10000000000000) -> int:
    """
    Converts each machine to a system of linear equations, and solves the puzzle.
    Leverages SymPy for speed.
    """
    total = 0    
    for aa, bb, tt in parse(src):
        sys = Matrix((
            (aa[0], bb[0], tt[0] + buffer),
            (aa[1], bb[1], tt[1] + buffer)
        ))
        sols = solve_linear_system(sys, a, b)
        if int(sols[a]) == sols[a] and int(sols[b]) == sols[b]:
            total += 3 * sols[a] + 1 * sols[b]
    return total


# Tests

given = \
"""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

def test_part_1():
    assert solve_machine(given, buffer=0) == 480

def test_part_2():
    assert solve_machine(given, buffer=0) == 875318608908