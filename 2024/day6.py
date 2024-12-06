import pandas as pd
import numpy as np
from io import StringIO
from tqdm import tqdm


def rotate(x: np.ndarray) -> np.ndarray:
    """
    Rotates and returns the given array according to the following pattern:
        
        [-1, 0] ->
        [0,  1] ->
        [1,  0] ->
        [0, -1] ->
        [-1, 0] -> 
        ...
    """
    if x[0] != 0:
        x[0] *= -1
    x = np.flip(x)
    return x

def step(pos: np.ndarray, direction: np.ndarray) -> np.ndarray:
    """Adds a direction vector to a position vector."""
    return np.add(pos, direction)

def path(map_: np.ndarray[np.ndarray], verbose=False) -> int:
    """
    Traces the path of the guard by accumulating a set of (pos-row, pos-col, dir-y, dir-x).
    Terminates if a combination of position and direction has been seen already,
    since this means the guard is stuck in a loop.
    
    params:
        map_: A 2D numpy array of [#.^].
        verbose: Print the current position and direction.
        
    returns:
        The length of the guard's walk before leaving the map.
        If the map contains a cycle, returns -1.
    """
    direction = [-1, 0] # vertical and horizontal direction
    pos = np.argwhere(map_ == '^')[0] # starting position
    next_step = step(pos, direction)
    rows, cols = map_.shape
    seen = set()
    
    while 0 <= next_step[0] < rows and 0 <= next_step[1] <= cols:
        if verbose:
            print(pos, direction)
        next_step = step(pos, direction)
        as_tuple = tuple([*pos, *direction])
        try:
            if as_tuple in seen:
                return -1 # guard is stuck in a loop!
            elif map_[*next_step] == '#':
                direction = rotate(direction)
            else:
                seen.add(as_tuple)
                pos = next_step
        except IndexError:
            seen.add(as_tuple)
            return len(seen)

def solve1(src: str, verbose=False) -> int:
    """Solves part 1, given either a filename or a map in string form."""
    map_ = pd.read_csv(src if src.endswith('.txt') else StringIO(src),
                       header=None, sep='', engine='python').dropna(axis=1).to_numpy()
    return path(map_, verbose=verbose)

def solve2(src: str, verbose=False) -> int:
    """Solves part 1, given either a filename or a map in string form."""
    map_ = pd.read_csv(src if src.endswith('.txt') else StringIO(src),
                       header=None, sep='', engine='python').dropna(axis=1).to_numpy()
    count = 0
    
    with tqdm(map_.size) as pbar: 
        for r in range(map_.shape[0]):
            for c in range(map_.shape[1]):
                if verbose > 0:
                    print(r, c)
                cur = map_[r, c]
                if cur == '.':
                    map_[r, c] = '#'
                    if path(map_, verbose=verbose > 1) == -1:
                        count += 1
                    map_[r, c] = 'cur'
                pbar.update(1)
    return count


# Tests

given = \
"""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

def test_part1():
    assert solve1(given) == 41

def test_part2():
    assert solve2(given) == 6
    