from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from abc import ABC, abstractmethod
from io import StringIO

from typing import Callable

class AOCrunner:
    """A runner for Advent of Code."""
    def __init__(self, inputfile: str, testcase: str, testcase2: str | None = None):
        self.inputfile = inputfile
        self.testcase = testcase
        self.testcase2 = testcase2
    
    def _test(self, part: int, solver: Callable, expected: int, *args, **kwargs) -> None:
        if part == 1:
            test_input = self.testcase
        else:
            test_input = self.testcase2 or self.testcase
        actual = solver(StringIO(test_input), *args, **kwargs)
        assert actual == expected, f"Part {part}: Expected {expected}, got {actual}."
        
    def _solve(self, part: int, solver: Callable, *args, **kwargs) -> None:
        with open(self.inputfile) as f:
            ans = solver(f, *args, **kwargs)
            print(f"Part {part}: {ans}")
    
    def testpart1(self, solver: Callable, expected: int, *args, **kwargs) -> None:
        """Use this method if test and solve have different inputs."""
        self._test(1, solver, expected, *args, **kwargs)
    
    def testpart2(self, solver: Callable, expected: int, *args, **kwargs) -> None:
        """Use this method if test and solve have different inputs."""
        self._test(2, solver, expected, *args, **kwargs)
    
    def solvepart1(self, solver: Callable, *args, **kwargs) -> None:
        """Use this method if test and solve have different inputs."""
        self._solve(1, solver, *args, **kwargs)
    
    def solvepart2(self, solver: Callable, *args, **kwargs) -> None:
        """Use this method if test and solve have different inputs."""
        self._solve(2, solver, *args, **kwargs)
    
    def part1(self, solver: Callable, expected: int, *args, **kwargs) -> None:
        """Use this method if test and solve have the same inputs."""
        self._test(1, solver, expected, *args, **kwargs)
        self._solve(1, solver, *args, **kwargs)
    
    def part2(self, solver: Callable, expected: int, *args, **kwargs) -> None:
        """Use this method if test and solve have the same inputs."""
        self._test(2, solver, expected, *args, **kwargs)
        self._solve(2, solver, *args, **kwargs)
    

class Posn(ABC):
    @abstractmethod
    def distance(self, other: Posn) -> float:
        pass


@dataclass(frozen=True)
class Posn2D(Posn):
    x: int
    y: int
        
    def __repr__(self):
        return f"({self.x}, {self.y})"
        
    def distance(self, other: Posn) -> float:
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)


@dataclass(frozen=True)
class Posn3D(Posn):
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def distance(self, other: Posn) -> float:
        return sqrt(
            (other.x - self.x) ** 2 + (other.y - self.y) ** 2 + (other.z - self.z) ** 2
        )


class Window:
    @staticmethod
    def slide_centered(arr, shape):
        """
        Yields a sliding window centered on each element of the array.
        The window will have maximum size equal to self.shape,
        but the size will be smaller around the edges.
        """
        assert shape[0] % 2 != 0, "Window dimensions must be odd!"
        assert shape[1] % 2 != 0, "Window dimensions must be odd!"

        row_offset = shape[0] // 2
        col_offset = shape[1] // 2
        n = len(arr)
        m = len(arr[0])
        for i in range(n):
            upper_row = max(0, i - row_offset)
            lower_row = min(n, i + row_offset)
            rows = arr[upper_row : lower_row + 1]
            for j in range(m):
                left_col = max(0, j - col_offset)
                right_col = min(m, j + col_offset)

                yield [row[left_col : right_col + 1] for row in rows]
                
"""
c = connect_circuits(StringIO(TESTCASE), 10, 3)
assert c == 40, f"Got {c}."

with open(INPUTFILE, "r") as f:
    print("Part 1:", connect_circuits(f, 1000, 3))

d = find_last_pair(StringIO(TESTCASE))
assert d == 25_272, f"Got {d}."

with open(INPUTFILE, "r") as f:
    print("Part 2:", find_last_pair(f))
"""
