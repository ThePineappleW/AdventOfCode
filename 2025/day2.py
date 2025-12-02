#! /usr/bin/python3
import re

INPUTFILE = r"inputs/day2.txt"
TESTCASE = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

def parse_input(s: str) -> list[list[int]]:
  """
  Splits the input on commas, then splits each range.
  Converts the input to [start, end] pairs of ints
  """
  return [[int(n) for n in rng.split("-")] for rng in s.split(",")]


def add_invalid_in_range(start: int, end: int, pattern: re.Pattern) -> int:
  """Finds each invalid item in a range, and adds them all together."""
  return sum(i for i in range(start, end + 1) if re.match(pattern, str(i)))


def sum_invalid(s: str, pattern: re.Pattern) -> int:
  """Computes the sum of all invalid items across a list of ranges."""
  return sum(add_invalid_in_range(*rng, pattern) for rng in parse_input(s))


double_pattern = re.compile(r"^(\d+)\1$")
more_pattern = re.compile(r"^(\d+)\1+$")


if __name__ == "__main__":
  
  
  assert sum_invalid(TESTCASE, double_pattern) == 1227775554
  
  with open(INPUTFILE, "r") as f:
    print("Part 1:", sum_invalid(f.read(), double_pattern))
    
  
  assert sum_invalid(TESTCASE, more_pattern) == 4174379265
  
  with open(INPUTFILE, "r") as f:
    print("Part 2:", sum_invalid(f.read(), more_pattern))
