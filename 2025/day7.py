#! /usr/bin/env python

from collections import defaultdict
from io import StringIO
import re

import networkx as nx

INPUTFILE = r"inputs/day7.txt"
TESTCASE = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""


def build_graph(f):
  G = nx.DiGraph()
  for row, level in enumerate(f):
    for col, symbol in enumerate(level):
      node = (row, col)
      above_node = (row - 1, col)
      if symbol == "S":
        G.add_node(node)
      
      if symbol == "." and above_node in G:
        G.add_edge(above_node, node)
      
      if symbol == "^" and above_node in G:
        G.add_edge(above_node, (row, col - 1))
        G.add_edge(above_node, (row, col + 1))
  return G

def count_split_beams(f, verbose=False) -> int:
  G = build_graph(f)
  n = len([deg for _, deg in  G.out_degree() if deg > 1])
  if verbose:
    print(n)
  return n

def count_paths(f, verbose=False):
  G = build_graph(f)
  nodes = (nx.topological_sort(G))
  root = next(nodes) # The first in topological order is the root. 
  leaves = (node for node, deg in G.out_degree() if deg == 0)
  
  
  # Store the number of paths from root to every node.
  memo = {root: 1}
  
  for node in nodes:
    memo[node] = sum(memo[parent] for parent in G.predecessors(node))
  
  return sum(memo[leaf] for leaf in leaves)
    
  

if __name__ == "__main__":
  c = count_split_beams(StringIO(TESTCASE), verbose=True)
  assert c == 21, f"Got {c}."
  
  with open(INPUTFILE, "r") as f:
    print("Part 1:", count_split_beams(f))
  
  c = count_paths(StringIO(TESTCASE), verbose=True)
  assert c == 40, f"Got {c}."
  
  with open(INPUTFILE, "r") as f:
    print("Part 2:", count_paths(f))
  
