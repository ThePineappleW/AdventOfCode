#! /usr/bin/python3

from utils import Window

from pprint import pprint
from io import StringIO

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



def parse(f):
  """Conver the input into a 2d matrix."""
  arr = []
  for line in f:
    arr.append([])
    for symbol in line.strip():
      arr[-1].append(symbol)
  return arr

def count_accessible(arr: list[list[str]]) -> int:
  rolls = []
  count = 0
  for i, (window, center_row, center_col) in enumerate(Window.slide_centered(arr, (3, 3))):
    if window[center_row][center_col] == '@':
      
      if sum(row.count("@") for row in window) < 5:
        count += 1
        
        coords = divmod(i, len(arr[0]))
        rolls.append(coords)
  return count, rolls

def remove_rolls(arr: list[list[str]]) -> int:
  accessible, rolls = count_accessible(arr)
  if accessible == 0:
    return 0
  
  for row, col in rolls:
    arr[row][col] = '.'
  return accessible + remove_rolls(arr)
  

def solve1(f) -> int:
  return count_accessible(parse(f))[0]

def solve2(f) -> int:
  return remove_rolls(parse(f))


if __name__ == "__main__":
  
  assert solve1(StringIO(TESTCASE)) == 13
  with open(INPUTFILE, "r") as f:
    print("Part 1:", solve1(f))


  assert solve2(StringIO(TESTCASE)) == 43
  with open(INPUTFILE, "r") as f:
    print("Part 2:", solve2(f))
