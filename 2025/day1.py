#! /usr/bin/python3

from io import StringIO

INPUT = r"inputs/day1.txt"
TESTCASE = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

class Dial:
  def __init__(self):
    self.val = 50
    self.zeros = 0
    self.all_zeros = 0
  
  def left(self) -> None:
    self.val = self.val - 1 if self.val else 99
  
  def right(self) -> None:
    self.val = self.val + 1 if self.val < 99 else 0
    
  def turn(self, instr: str) -> None:
    direction = instr[0]
    amount = int(instr[1:])
    
    for _ in range(amount):
      if direction == 'L':
        self.left()
      else:
        self.right()
      if self.val == 0:
        self.all_zeros += 1
    if self.val == 0:
      self.zeros += 1


def count_zeros(instrs) -> tuple[int, int]:
  d = Dial()
  for instr in instrs:
    d.turn(instr)
  return d.zeros, d.all_zeros
    
    
if __name__ == "__main__":
  assert count_zeros(StringIO(TESTCASE)) == (3, 6)
  
  with open(INPUT, "r") as f:
    print("Part 1: {}\nPart 2: {}".format(*count_zeros(f)))
