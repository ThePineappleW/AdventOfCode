import pandas as pd
import numpy as np
from io import StringIO
from math import gcd


def get_input(src:str) -> pd.DataFrame:
    if not src.endswith('.txt'):
        src = StringIO(src)
    return pd.read_csv(src, sep=r'', header=None, engine='python').dropna(axis=1).to_numpy()


def cart_dist(p1: tuple[int], p2: tuple[int]) -> tuple[int]:
    """The change in X and Y between two points."""
    return p1[0] - p2[0], p1[1] - p2[1] 


def all_nodes(arr: np.ndarray, r: int, c: int) -> tuple[np.ndarray]:
    """
    Returns a list of row and column coordinates for each node with the same marker as the given type.
    """
    if arr[r, c] == '.':
        return np.array([]), np.array([])
    else:
        return np.where(arr == arr[r, c])


def points_in_line(arr: np.ndarray, r1: int, c1: int, r2: int, c2: int, harmonics=True) -> list[tuple[int]]:
    """
    Gets points in line with `(r1, c1)` with slope `(r2, c2)`.
    If `harmonics`, get all points in this line.
    If not, find a single point in line with the two given points, 
    twice as far as from `(r1, c1)` as from `(r2, c2)`.

    Respects the boundaries of `arr`.

    arr: The map.
        r1, c1: The row, column coordinates of the first point.
        r2, c2: The row, column coordinates of the second point.
        harmonics: Count all nodes in a line?

    returns:
        The set of all valid (row, col) points.
    """
    if r1 == r2 and c1 == c2:
        return set() # Exit if comparing a point to itself.
    
    nrows, ncols = arr.shape
    dr, dc = cart_dist((r1, c1), (r2, c2)) # dr = distance_r 
    val = arr[r1, c1]
    if harmonics:
        gcd_ = gcd(dr, dc)
        sr, sc = int(dr / gcd_), int(dc / gcd_) # sr = slope_r


        
        points = set()
        r, c = r1, c1
        for _ in range(max(nrows, ncols)):
            r, c = r + sr, c + sc
            if 0 <= r < nrows and 0 <= c < ncols:
                points.add((r, c))
            
            rneg, cneg = r - sr, c - sc
            if 0 <= rneg < nrows and 0 <= cneg < ncols:
                points.add((rneg, cneg))

        return points
    else:
        # Just a single point.
        r, c = r1 + dr, c1 + dc
        if 0 <= r < nrows and 0 <= c < ncols:
            return {(r, c)}
        else:
            return set()

def antinodes(arr: np.ndarray, r: int, c: int, harmonics=True) -> set[tuple[int]]:
    """
    Returns a list of row and column coordinates for each antinode for the given location.

    params:
        arr: The map.
        r, c: The row, column coordinates of the point.
        harmonics: Count all nodes in a line?

    returns:
        The set of all (row, col) antinodes.
    """
    nrows, ncols = arr.shape
    nodes = list(zip(*all_nodes(arr, r, c)))
    antinodes = set()
    for node in nodes:
        points = points_in_line(arr, r, c, *node, harmonics=harmonics)
        antinodes = antinodes.union(points)
    # antinodes = antinodes.difference(nodes)
    return antinodes
    

def total_antinodes(src: str, harmonics=True, debug=False) -> int:
    """
    Coujnts the number of antinodes in the input.
    
    params:
        src: Input source.
        harmonics: Count all nodes in a line?
        debug: Return the set of nodes, instead of the count.
    """
    arr = get_input(src)
    found_antinodes = set()
    for r, c in zip(*np.where(arr != '.')):
        found_antinodes = found_antinodes.union(antinodes(arr, r, c, harmonics=harmonics))

    if debug:
        return found_antinodes
    else:
        return len(found_antinodes)


# Just for fun...
def disp_antinodes(str, **kwargs):
    """Draw Antinodes onto the map."""
    arr2 = get_input(str)
    an = total_antinodes(str, debug=True, **kwargs)
    for p in an:
        if arr2[int(p[0]), int(p[1])] == '.':
            arr2[int(p[0]), int(p[1])] = '#'
    print(f'\n'.join([''.join(r) for r in arr2]))


# Tests

given = \
"""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

def test_part1():
    assert total_antinodes(given, harmonics=False) == 14

def test_part2():
    assert total_antinodes(given, harmonics=True) == 34