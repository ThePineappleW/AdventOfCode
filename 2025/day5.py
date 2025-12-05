#! /usr/bin/env python

from bisect import bisect
from io import StringIO

from intervaltree import IntervalTree


INPUTFILE = r"inputs/day5.txt"
TESTCASE = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

def parse_ranges(s: str) -> list[tuple[int, int]]:
  """Converts ranges to integer tuples, adjusting the end bound to be exclusive."""
  ranges = []
  for line in s.split("\n"):
    left, right = line.strip().split("-")
    ranges.append((int(left), int(right) + 1))
  return ranges


def parse_ids(s: str) -> list[int]:
  """Converts string IDs into integers."""
  return [int(line) for line in s.split("\n") if line]


def parse(f) -> tuple[list[tuple[int, int]], list[int]]:
  """Converts the input file into a list of ranges and a list of ids."""
  ranges, ids = f.read().split("\n\n")
  return parse_ranges(ranges), parse_ids(ids)


def count_fresh(f) -> int:
  """
  Counts the number of IDs which occur within at least one of the intervals.
  Uses an Interval Tree to do this efficiently.
  https://en.wikipedia.org/wiki/Interval_tree
  """
  ranges, ids = parse(f)
  tree = IntervalTree.from_tuples(ranges)
  return len([id_ for id_ in ids if tree[id_]])
    

def total_fresh(f) -> int:
  """
  Counts the number of distinct points which occur within any of the intervals.
  The approach is to put all the intervals into an Interval Tree,
  then to transform the tree by merging all overlapping intervals.
  
  This results in an equivalent set of non-overlapping intervals, 
  which we can then count.
  """
  ranges, _ = parse(f)
  tree = IntervalTree.from_tuples(ranges)
  tree.merge_overlaps()
  
  total = 0
  for (begin, end, _) in tree:
    total += end - begin
  return total


if __name__ == "__main__":
  assert count_fresh(StringIO(TESTCASE)) == 3
  with open(INPUTFILE, "r") as f:
    print("Part 1:", count_fresh(f))
    
  assert total_fresh(StringIO(TESTCASE)) == 14
  with open(INPUTFILE, "r") as f:
    print("Part 1:", total_fresh(f))


  
