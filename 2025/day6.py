#! /usr/bin/python3

from io import StringIO
from math import prod
from pprint import pprint

INPUTFILE = "inputs/day6.txt"
TESTCASE = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

symbol_to_op = {"+" : sum, "*" : prod}

def parse_symbol(s: str):
  return symbol_to_op[s] if s in symbol_to_op else int(s)

def parse_normal(f):
  return zip(*[[parse_symbol(item) for item in row.split()] for row in f])

def parse_cephalopod(f):
  rows = list(zip(*[reversed(row.strip("\n")) for row in f]))
  ops = [symbol_to_op[row[-1]] for row in rows if row[-1] != " "]
  rows = ["".join(row[:-1]) for row in rows]
  nums = [[]]
  for str_ in rows:
    if str_.strip() == "":
      nums.append([])
    else:
      nums[-1].append(int(str_))
  for num_list in nums:
    num_list.append(ops.pop(0))
  return nums

def compute(f, parser, verbose=False):
  rows = list(parser(f))
  if verbose:
    print(rows)
  return sum(row[-1](row[:-1]) for row in rows)

if __name__ == "__main__":
  assert compute(StringIO(TESTCASE), parse_normal) == 4277556
  with open(INPUTFILE, "r") as f:
    print("Part 1:", compute(f, parse_normal))
  
  assert compute(StringIO(TESTCASE), parse_cephalopod) == 3263827
  with open(INPUTFILE, "r") as f:
    print("Part 2:", compute(f, parse_cephalopod))
  
