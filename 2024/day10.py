import pandas as pd
import numpy as np
from io import StringIO
import networkx as nx
# import matplotlib.pyplot as plt


class Spot:
    """Represents a spot on the topographic map."""
    def __init__(self, elev:int, row:int, col:int):
        # Record coordinates for future vizualization
        self.elev = elev
        self.row = row
        self.col = col

    def __repr__(self):
        return self.elev.__repr__()


def get_input(src:str) -> np.ndarray[Spot]:
    """
    Grab input from a string/filename.

    Put it into a Numpy array of Spots. 
    """
    
    if not src.endswith('.txt'):
        src = StringIO(src)
    grid = pd.read_csv(src, header=None, sep='', engine='python').dropna(axis=1).to_numpy(dtype='object')
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            grid[r,c] = Spot(grid[r, c], r, c)
    return grid


def array2graph(spots:np.ndarray) -> nx.Graph[Spot]:
    """Convert a spot array into a DAG, where each edge increases elevation by one."""
    G = nx.DiGraph()
    dirs = ((-1,0),(1,0),(0,-1),(0,1))
    rows, cols = spots.shape
    for r in range(rows):
        for c in range(cols):
            node = spots[r, c]
            for dr, dc in dirs:
                rd, cd = r + dr, c + dc
                if 0 <= rd < rows and 0 <= cd < cols:
                    other = spots[rd, cd]
                    if other.elev - node.elev == 1:
                        G.add_edge(node, other)
    return G


def trailheads(G: nx.Graph) -> list[Spot]:
    """Get all trailheads (elevation = 0) for a graph."""
    return [n for n in G.nodes if n.elev == 0]


def score(src:str) -> tuple[int]:
    """
    Takes the input source string.
    Computes scores for both parts.

    Returns:
        Part 1 score, Part 2 score
    
    """
    G = array2graph(get_input(src))
    p1_total, p2_total = 0, 0
    for head in trailheads(G):
        ends = nx.descendants_at_distance(G, head, 9)
        p1_total += len(ends)
        for end in ends:
            p2_total += len(list(nx.all_shortest_paths(G, head, end)))
    return p1_total, p2_total


# Tests

given = \
"""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

def test_part_1():
    assert score(given)[0] == 36

def test_part_2():
    assert score(given)[1] == 81