#! /usr/bin/python3

from io import StringIO

INPUTFILE = r"inputs/day3.txt"
TESTCASE = """987654321111111
811111111111119
234234234234278
818181911112111"""
  
def argmax(lst: list[int]) -> tuple[int, int]:
  """Returns the index and the value of the greatest element in the list."""
  return max(enumerate(lst), key= lambda x: x[1])

def max_two_digits(lst: list[int]) -> int:
  idx, left = argmax(lst[:-1])
  _, right = argmax(lst[idx + 1:])
  result = 10 * left + right
  print(result)
  return result

def max_n_digits(digit: list[int], n: int, verbose=False) -> int:
  """
  Returns the greatest n-digit number  that can be constructed
  from the provided list of digits, left-to-right.
  """
  total = 0
  left_bound = 0
  for i in range(n):
    power = 10 ** (n - i - 1)
    right_bound = -(n - i) + 1 or None
    idx, digit = argmax(digits[left_bound : right_bound])
    if verbose:
      print(left_bound, ":", right_bound)
    left_bound = left_bound + idx + 1
    total += digit * power
  if verbose:
    print(total)
  return total
    

def parse_file(f):
  """Splits the input file into lists of integers."""
  for line in f:
    yield [int(n) for n in line.strip()]


def sum_joltages(f, n:int, verbose=False) -> int:
  """Finds the total joltage for a file-like containing battery levels."""
  return sum(max_n_digits(nums, n, verbose=verbose) for nums in parse_file(f))


if __name__ == "__main__":
  
  assert sum_joltages(StringIO(TESTCASE), 2) == 357
  with open(INPUTFILE, "r") as f:
    print("Part 1:", sum_joltages(f, 2))
  
  assert sum_joltages(StringIO(TESTCASE), 12) == 3121910778619
  with open(INPUTFILE, "r") as f:
    print("Part 2:", sum_joltages(f, 12))
  
  
