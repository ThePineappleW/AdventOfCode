#! /usr/bin/python3

import math
import re

from itertools import combinations

from typing import Iterable, TypeVar

from utils import AOCrunner, Posn3D

INPUTFILE = r"inputs/day8.txt"
TESTCASE = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


def parse(f) -> Iterable[Posn3D]:
    pattern = re.compile(r"^(\d+),(\d+),(\d+)$")
    for line in f:
        x, y, z = pattern.match(line).groups()
        yield Posn3D(int(x), int(y), int(z))


def sorted_pairs(junctions: list[Posn3D]) -> Iterable[tuple[Posn3D, Posn3D]]:
    pairs = combinations(junctions, 2)
    return sorted(pairs, key=lambda x: x[0].distance(x[1]))


T = TypeVar("T")


class DisjointSet:
    """
    Represents a disjoint set, AKA a Union/Find,
    to implement Kruskal's Algorithm.
    """

    def __init__(self, nodes: Iterable[T]):
        self.parents = {}  # The set of "blobs" in the data structure.
        self._sizes = {}

        for node in nodes:
            self.make_set(node)

    def roots(self) -> list[T]:
        return [node for node, parent in self.parents.items() if node == parent]

    def sizes(self) -> list[int]:
        return sorted(
            [
                self._sizes[node]
                for node, parent in self.parents.items()
                if node == parent
            ],
            reverse=True,
        )

    def make_set(self, node: T) -> None:
        if node not in self.parents:
            self.parents[node] = node
            self._sizes[node] = 1

    def find(self, node: T) -> T:
        parent = self.parents[node]
        if parent != node:
            self.parents[node] = self.find(parent)
            return self.parents[node]
        else:
            return node

    def union(self, node1: T, node2: T) -> T:
        """
        Attempt to merge two nodes by size.
        Returns the new parent, or None if they are already merged.
        """
        x = self.find(node1)
        y = self.find(node2)

        if x == y:
            return None

        # Ensure that size(x) >= size(y)
        if self._sizes[x] < self._sizes[y]:
            x, y = y, x

        self.parents[y] = x
        self._sizes[x] += self._sizes[y]
        return x

    def connect(self, node1: T, node2: T) -> bool:
        u = self.union(node1, node2)
        return bool(u)


def connect_circuits(f, n_connections: int, top_n: int = 3) -> int:
    junctions = list(parse(f))
    ds = DisjointSet(junctions)

    for j1, j2 in sorted_pairs(junctions)[:n_connections]:
        ds.connect(j1, j2)

    return math.prod(ds.sizes()[:top_n])


def find_last_pair(f) -> int:
    junctions = list(parse(f))
    ds = DisjointSet(junctions)
    n = len(junctions) - 1

    count = 0
    for j1, j2 in sorted_pairs(junctions):
        if ds.connect(j1, j2):
            count += 1
        if count == n:
            return j1.x * j2.x


if __name__ == "__main__":
    aoc = AOCrunner(INPUTFILE, TESTCASE)
    
    aoc.testpart1(connect_circuits, 40, 10)
    aoc.solvepart1(connect_circuits, 1000)
    
    aoc.testpart2(find_last_pair, 25_272)
    aoc.solvepart2(find_last_pair)
