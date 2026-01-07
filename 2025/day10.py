#! /usr/bin/env python

import re

from typing import Iterable

from utils import AOCrunner

from sympy import solve, simplify, Dummy

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


INPUTFILE = r"inputs/day10.txt"
TESTCASE = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


class Button:
    def __init__(self, slots: Iterable[int]):
        self.slots = tuple(slots)

    def toggle_lights(self, lights: tuple[bool]) -> tuple[bool]:
        return tuple(
            [
                not light if slot in self.slots else light
                for slot, light in enumerate(lights)
            ]
        )

    def toggle_joltages(self, joltages: tuple[bool]) -> tuple[bool]:
        return tuple(
            [
                jolt + 1 if slot in self.slots else jolt
                for slot, jolt in enumerate(joltages)
            ]
        )


def parse_lights(s: str) -> tuple([bool]):
    return tuple([char == "#" for char in s.strip("[]")])


def parse_button(s: str) -> Button:
    return Button([int(num) for num in s.strip("()").split(",")])


def parse_joltages(s: str) -> tuple[int]:
    return tuple([int(num) for num in s.strip("{}").split(",")])


def parse(f):
    lights_pattern = re.compile(r"\[[\.#]+\]")
    button_pattern = re.compile(r"\([\d,]+\)")
    joltage_pattern = re.compile(r"\{(\d+,?)+\}")
    for line in f:
        lights_match = lights_pattern.search(line).group()
        buttons_matches = button_pattern.findall(line)
        joltages_match = joltage_pattern.search(line).group()

        lights = parse_lights(lights_match)
        buttons = [parse_button(match) for match in buttons_matches]
        joltages = parse_joltages(joltages_match)

        yield lights, buttons, joltages


def turn_on_lights(target_lights: tuple[bool], buttons: list[Button]) -> int:
    """
    Dynamic programming function that finds the minimum steps to turn on
    the appropriate lights.

    Here's pseudocode for a recursive version.
    It returns the number of steps to reach the target.

    turn_on(current, target, buttons) -> int:
        if current == target:
            return 0
        else:
            num_steps = []
            for button in buttons:
                n = turn_on(button.toggle(current), target, buttons)
                num_steps.append(n)
            return min(n)

    The DP approach instead builds up a memo table with all reachable states
    for each successive number of steps.

    We can avoid duplication by using sets instead of lists.
    By keeping track of observed states, we can avoid including states that are repeated at later steps.
    """
    starting_lights = (False,) * len(target_lights)

    seen = set([starting_lights])
    memo = [set([starting_lights])]

    while True:
        prev_states = memo[-1]
        memo.append(set())
        for prev_state in prev_states:
            for button in buttons:
                new_state = button.toggle_lights(prev_state)
                if new_state == target_lights:
                    return len(memo) - 1

                if new_state not in seen:
                    seen.add(new_state)
                    memo[-1].add(new_state)


def turn_on_all_lights(f) -> int:
    return sum(turn_on_lights(lights, buttons) for lights, buttons, _ in parse(f))


def configure_joltages_v1(target_joltages: tuple[int], buttons: list[Button]) -> int:
    """
    First attempt: Same algorightm as part 1. This is very slow.
    """

    starting_joltages = (0,) * len(target_joltages)

    seen = set([starting_joltages])
    memo = [set([starting_joltages])]

    while True:
        prev_states = memo[-1]
        memo.append(set())
        for prev_state in prev_states:
            for button in buttons:
                new_state = button.toggle_joltages(prev_state)
                if new_state == target_joltages:
                    return len(memo) - 1

                if new_state not in seen and new_state <= target_joltages:
                    seen.add(new_state)
                    memo[-1].add(new_state)


def configure_joltages_v2(
    target_joltages: tuple[int], buttons: list[Button], verbose=False
) -> int:
    """
    Second attempt: Treat this as a linear system of equations and find the minimum solution.
    Problem: Need to enforce non-negativity on the variables.
    """
    var_map = {i: Dummy(chr(i + 65)) for i in range(len(buttons))}
    eqs = []
    for slot, target in enumerate(target_joltages):
        eq = -target
        for i, button in enumerate(buttons):
            if slot in button.slots:
                eq = var_map[i] + eq
        eqs.append(eq)

    if verbose:
        for eq in eqs:
            print(eq)
        print()

    solutions = solve(eqs, list(var_map.values()), dict=True)
    if verbose:
        print(solutions)

    steps = []
    for solution in solutions:
        total = simplify(sum(solution.values()))
        if verbose:
            print(total)
            print()
        steps.append(total)
    return min(steps)


def configure_joltages(
    target_joltages: tuple[int], buttons: list[Button], verbose=False
) -> int:
    """
    Third attempt: Linear programming.
    Problem: Need to exclude fractional values.

    Fourth attempt: Mixed-integer linear programming.
    """
    m = len(target_joltages)
    n = len(buttons)

    # Ax = b
    A = np.array([[int(i in button.slots) for button in buttons] for i in range(m)])
    b = np.array(target_joltages)
    c = np.ones(n)
    if verbose:
        print(A)
        print(b)
        print(c)

    # Third attempt:
    # solution = linprog(c, A, b, A_eq=A, b_eq=b, bounds=(0, None))

    # Fourth attempt:
    solution = milp(
        c, constraints=LinearConstraint(A, b, b), integrality=c, bounds=Bounds(0, 1000)
    )

    if verbose:
        print(solution.x, "==>", sum(solution.x))
        print()
    total = sum(solution.x)
    assert int(total) == total, total
    return int(total)


def configure_all_joltages(f, verbose=False) -> int:
    return sum(
        configure_joltages(jolts, buttons, verbose=verbose)
        for _, buttons, jolts in parse(f)
    )


if __name__ == "__main__":
    aoc = AOCrunner(INPUTFILE, TESTCASE)
    aoc.part1(turn_on_all_lights, 7)
    aoc.part2(configure_all_joltages, 33, verbose=False)
