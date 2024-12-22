from re import findall
from collections import defaultdict
from math import prod
from pprint import pprint as pp

import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm.autonotebook import tqdm

"""
Part 1 was pretty simple (though I lost a lot of time by forgetting to parse the negative sign).

Part 2 was really fun. I made a bunch of scatterplots to manually find the tree, which was pretty cool.
"""

def print_robots(bots:list, nrows:int, ncols:int) -> None:
    """Visualization function."""
    board = np.zeros((nrows, ncols))
    for bot in bots:
        r, c = bot.pos()
        board[r, c] += 1
    
    s = str(board).replace('.', '')
    s = s.replace('0', '.')
    pp(s)
    print()


class Robot:
    """Stores a position and a velocity."""
    def __init__(self, c:int, r:int, vc:int, vr:int):
        self.c, self.r = c, r
        self.vc, self.vr = vc, vr

    def pos(self) -> tuple[int]:
        """Note that positions are given column-first, but returned row-first. I prefer it this way."""
        return self.r, self.c
    
    def simulate(self, t:int, nrows:int, ncols:int, verbose=False) -> tuple[int]:
        """Updates the position and velocity"""
        for _ in range(t):
            self.r = (self.r + self.vr) % nrows
            self.c = (self.c + self.vc) % ncols
            if verbose:
                print_robots([self], nrows, ncols)
                print()
        return self.pos()


def nums(s: str) -> list[int]:
    """Parses numbers out of a string."""
    return [int(d) for d in findall(r'-?\d+', s)]


def parse(src: str) -> list[Robot]:
    """
    Consumes a standard source string.
    Converts it into a list of Robots.
    """
    if src.endswith('.txt'):
        with open(src, 'r') as f:
            lines = f.readlines()
    else:
        lines = src.split('\n')

    return [Robot(*nums(l)) for l in lines]


def groupby(lst: list, key: callable) -> dict:
    """Standard groupby. Maybe I should make a utils module..."""
    output = defaultdict(list)
    for item in lst:
        output[key(item)].append(item)
    return dict(output)


def safety_factor(src:str, t:int, nrows:int, ncols:int, verbose=False) -> int:
    """Computes the safety factor after `t` seconds."""
    bots = parse(src)
    for b in bots:
        b.simulate(t, nrows, ncols)

    def quad(bot):
        """Returns a unique tuple (or -1) corresponding to the quandrant of this robot."""
        r, c = bot.pos()
        hr = nrows // 2
        hc = ncols // 2
        if r == hr or c == hc:
            return -1
        else:
            return (r < hr, c < hc)
            
    quads = groupby(bots, quad)
    if verbose:
        print_robots(bots, nrows, ncols)
    
    return prod([len(v) for k, v in quads.items() if k != -1])


def is_tree(bots: list[Robot], i:int=None, k=8, min_cluster=62,  verbose=False, **kwargs) -> int:
    """
    My thought process for finding a picture of a tree:
    - I don't know what a "Christmas Tree" looks like. Maybe if it were a chanukkiah, on the other hand...
    - Most of the robots in the tree will be clustered together, I assume.
    - Use KMeans to look through 10k generations.
    - Pick (and maybe manually inspect) the ones with the largest clusters.

    Params:
        - bots: the robots
        - i: the number of seconds elapsed before this iteration. Only needed if verbose.
        - k: number of KMeans clusters.
        - min_clusters: threshold number of bots for a cluster to be a candidate for tree. Should be > `len(bots) / k`.
        - verbose: Plot the bots if they are candidates for a tree!

    Returns:
        The number of bots in the largest cluster.
        If the tree exists, this usually represents it.
    """
    data = np.array([b.pos() for b in bots])
    km = KMeans(k, **kwargs)
    clusters = km.fit_predict(data)
    count = Counter(clusters)
    max_cluster = count.most_common()[0][1]
    if verbose and max_cluster >= min_cluster:
        sns.scatterplot(y=data[:,0], x=data[:,1], hue=clusters, palette='viridis')
        plt.title(f'{i} seconds')
        plt.show()
    return max_cluster


def find_tree(src:str, nrows=103, ncols=101, max_iter=10_000, verbose=False, **kwargs) -> int:
    """
    Tests the above function on every generation in order to find the tree.

    Params:
        - src: A standard source string.
        - nrows, ncols: Size of grid.
        - max_iter: Number of iterations to test.
        - verbose: Plot every candidate iteration.

    Returns:
        The iteration which had the largest single cluster.
    """
    bots = parse(src)
    trees = []
    for i in tqdm(range(1, max_iter + 1)):
        for b in bots:
            b.simulate(1, nrows, ncols)
        trees.append((is_tree(bots, i, verbose=verbose, **kwargs), i))
    return list(sorted(trees, reverse=True))[0][1]


# Tests

given = \
"""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

def test_part_1():
    assert safety_factor(given) == 12

# Can't really test part 2 without exposing the full input.
# I recommend running it yourself.