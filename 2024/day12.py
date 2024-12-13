import pandas as pd
import numpy as np
import networkx as nx

from io import StringIO
from collections import defaultdict


def get_input(src:str) -> np.ndarray:
    """Unremarkable."""
    src = src if src.endswith('.txt') else StringIO(src)
    arr = pd.read_csv(src, sep='', engine='python', header=None).dropna(axis=1).to_numpy()
    return arr


def arr2graphs(arr: np.ndarray) -> nx.Graph:
    """
    Consumes a 2D array of letters.

    Returns two graphs:
    1) A graph with edges between adjacent intra-region nodes.
    2) A graph with edges between adjacent inter-region nodes (and array boundaries).
    """
    regions = nx.Graph()
    faces = nx.Graph()
    rows, cols = arr.shape
    for r in range(rows):
        for c in range(cols):
            node = (r, c, arr[r, c])
            regions.add_node(node)
            faces.add_node(node)
            # Add an edge between neighbors if they are the same kind of plant.
            if r > 0:
                if r == rows-1:
                    faces.add_edge(node, (rows, c, 'LOWER'))
                above = (r-1, c, arr[r - 1, c])
                if above[2] == node[2]:
                    regions.add_edge(node, above)
                else:
                    faces.add_edge(node, above)
            else:
                faces.add_edge(node, (-1, c, 'UPPER'))
            
            if c > 0:
                if c == cols-1:
                    faces.add_edge(node, (r, cols, 'RIGHT'))
                left = (r, c-1, arr[r, c - 1])
                if left[2] == node[2]:
                    regions.add_edge(node, left)
                else:
                    faces.add_edge(node, left)
            else:
                faces.add_edge(node, (r, -1, 'LEFT'))
                
            
    return regions, faces


def regions(G: nx.Graph) -> list[nx.Graph]:
    """Get the regions of stored in a graph."""
    return [G.subgraph(c) for c in nx.connected_components(G)]


def score_perim(region: nx.Graph) -> int:
    """What is the area*perimeter score of this region?"""
    area = region.number_of_nodes()
    perimeter = sum([4 - len(region.edges(n)) for n in region.nodes])
    return area * perimeter


def group_adjacent(items: list, key: callable) -> list[list]:
    """Segments `items` into sequential groups, such that `key(x) - key(y) = 1."""
    items = list(sorted(items, key=key))
    groups = [[]]
    for item in items:
        if (groups[-1] == []
            or key(item) - key(groups[-1][-1]) == 1):
            groups[-1].append(item)
        else:
            groups.append([item])
    return groups


def groupby(items: list, key: callable) -> list[list]:
    """Returns a dict of items grouped by the result of `key(item)`."""
    groups = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    return dict(groups)
    


def count_faces(faces: list[tuple], kind: 'h|v') -> int:
    """
    Given a list of face edges, and the direction of the faces, 
    Returns the number of sides present.
    Note that a 'face' is perpendicular to its edge. 
    So an edge between two nodes in the same column is vertical.


    The algorithm is simple:
        1) Group edges by row/column (based on `kind`).
        2) Group adjacent edges in that set, e.g. [ . _ _ . _ .]
        3) Add up the number of adjacent groups.
    """
    total = 0
    sort_key, group_key = (0, 1) if kind == 'h' else (1, 0)
    
    sorted_faces = list(groupby(faces, lambda f: (f[0][sort_key], f[1][sort_key])).values())
    
    for group in sorted_faces: 
        total += len(group_adjacent(group, lambda f: f[0][group_key]))
    return total


def count_sides(region: nx.Graph, faces: nx.Graph) -> int:
    """How many sides does this region have, given the faces graph?"""
    vfaces, hfaces = [], []
    for edges in [faces.edges(node) for node in region.nodes]:
        for edge in edges:
            node, other = edge
            if node[0] == other[0]: # Same row --> vertical face ( x | y )
                vfaces.append(edge)
            else:
                hfaces.append(edge)
    return count_faces(vfaces, 'v') + count_faces(hfaces, 'h')
 


def score_sides(region: nx.Graph, faces: nx.Graph) -> int:
    """What is the area*sides score of this region, given the faces graph?"""
    area = region.number_of_nodes()
    sides = count_sides(region, faces)
    return area * sides


def fence_prices(src: str) -> int:
    """Returns answers for both parts."""
    region_graph, faces = arr2graphs(get_input(src))
    regs = regions(region_graph)
    perim = sum([score_perim(r) for r in regs])
    sides = sum([score_sides(r, faces) for r in regs])
    return perim, sides


## Tests

given = \
"""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

def test_part_1():
    assert fence_prices(given)[0] == 1930

def test_part_2():
    assert fence_prices(given)[1] == 1206