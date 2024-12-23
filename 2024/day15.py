import pandas as pd
import numpy as np
from io import StringIO

from tqdm.autonotebook import tqdm

"""
I wanted to do a nice, abstracted approachwhere each BigBox was composed of two small boxes.
This was unfortunately annoying so I decided to just rewrite the all functions :(
"""

class Box:
    def __init__(self, r: int, c: int, verbose=False):
        self.r = r
        self.c = c
        self.verbose = True

    def pos(self) -> list[tuple[int]]:
        """The row, col position of this object."""
        return [(self.r, self.c)]
        

    def _neighbors(self, grid, direction: tuple[int]) -> set:
        """Get the object(s) directly adjacent to this one in the given direction."""
        next_poss = [np.add(p, direction) for p in self.pos()]
        neighbors =  set([grid.get(p) for p in next_poss])
        if None in neighbors: 
            neighbors.remove(None)
        return neighbors
    
    def can_move(self, grid, direction: tuple[int]) -> bool:
        """
        Can this object move in the given direction?
        
        Params:
            Grid: A wrapper for all of the objects on the map.
            direction: A double (dr, dc), 
                       where each represents the direction of movement over the rows or columns respectively.
                       Assume that exactly one of dr, dc will be 0, and that both will be -1 <= n <= 1.
        """
        return all([n.can_move(grid, direction) for n in self._neighbors(grid, direction)])

    def _update_grid(self, grid, direction: tuple[int]) -> None:
        for p in self.pos():
            if grid.get(p):
                grid.remove(p)
        self.r, self.c = np.add(self.pos()[0], direction)
        for p in self.pos():
            grid.set(p, self)
    
    def move(self, grid, direction: tuple[int]) -> None:
        if self.can_move(grid, direction):
            for n in self._neighbors(grid, direction):
                n.move(grid, direction)
            self._update_grid(grid, direction)
            
    
    def score(self):
        return self.r * 100 + self.c

    def __repr__(self):
        return f'[{self.r}, {self.c}]'


class BigBox(Box):
    def __init__(self, r1: int, c1: int, r2: int, c2: int, verbose=False):
        self.left  = (r1, c1)
        self.right = (r2, c2)

    def pos(self):
        return [self.left, self.right]
    
    def _neighbors(self, grid, direction):
        next_poss = [np.add(p, direction) for p in self.pos()]
        neighbors = set([grid.get(p) for p in next_poss])
        neighbors -= {None, self}
        return neighbors

    def _update_grid(self, grid, direction: tuple[int]) -> None:
        for p in self.pos():
            grid.remove(p)
        self.left = np.add(self.left, direction)
        self.right = np.add(self.right, direction)
        for p in self.pos():
            grid.set(p, self)
    
    def move(self, grid, direction):
        if self.can_move(grid, direction):
            for n in self._neighbors(grid, direction):
                n.move(grid, direction)
            self._update_grid(grid, direction)

    def score(self):
        return self.left[0] * 100 + self.left[1]
    
    def __repr__(self):
        return str(self.pos())


class Border(Box):
    def __init__(self, r: int, c: int, verbose=False):
        super().__init__(r, c, verbose)

    def can_move(self, blocks, direction): return False
    def move(self, blocks, direction): raise RuntimeError("Borders can't move.")
    def score(self): return 0
    def __repr__(self):
        return f'#{self.r}, {self.c}#'


class Grid:
    def __init__(self, blocks: list[Box], player_pos: tuple[int], verbose=False):
        self.verbose = verbose
        self.moves = {
                '^': (-1, 0),
                'v': ( 1, 0),
                '<': (0, -1),
                '>': (0,  1)
            }
        self.player_pos = player_pos
        self.map = {}
        for block in blocks:
            poss = block.pos()
            for pos in poss:
                self.map[tuple(pos)] = block
        self.nrows = max([p[0] for p in self.map.keys()]) + 1
        self.ncols = max([p[1] for p in self.map.keys()]) + 1

    def __repr__(self):
        out = []
        open_box = False
        for r in range(self.nrows):
            for c in range(self.ncols):
                obj = self.get((r, c))
                if np.all((r, c) == self.player_pos):
                    out.append('@')
                elif isinstance(obj, Border):
                    out.append('#')
                elif isinstance(obj, BigBox):
                    out.append(']' if open_box else '[')
                    open_box = not open_box
                elif isinstance(obj, Box):
                    out.append('O')
                else:
                    out.append('.')
            out.append('\n')
        return ''.join(out)
    
    def get(self, pos: tuple[int]) -> Box:
        return self.map.get(tuple(pos), None)

    def set(self, pos: tuple[int], val: Box) -> None:
        self.map[tuple(pos)] = val
    
    def remove(self, pos: tuple[int]) -> None:
        del self.map[tuple(pos)]

    def apply_moves(self, moves: str):
        for arrow in tqdm(moves):
            if arrow != '\n':
                move = self.moves[arrow]
                next_pos = np.add(self.player_pos, move)
                adj = self.get(next_pos)
                if self.verbose:
                    print(adj)
                if adj is None:
                    self.player_pos = next_pos
                elif adj.can_move(self, move):
                    adj.move(self, move)
                    self.player_pos = next_pos
            if self.verbose:
                print('Move:', arrow)
                print(self)

    def score(self):
        return sum([o.score() for o in set(self.map.values())])


def enwiden(map_: str) -> str:
    """Widens the map according to the given rules."""
    map_ = map_.replace('#', '##')
    map_ = map_.replace('O', '[]')
    map_ = map_.replace('.', '..')
    map_ = map_.replace('@', '@.')
    return map_


def parse(map_src: str, widen=False, verbose=False) -> (list[Box], tuple[int]):
    """Returns a list of objects, and the position of the player."""
    if map_src.endswith('.txt'):
        with open(map_src, 'r') as f:
            map_ = f.read()
    else:
        map_ = map_src
    
    if widen:
        map_ = enwiden(map_)
    
    arr = pd.read_csv(StringIO(map_), header=None, engine='python', sep='').dropna(axis=1).to_numpy()
    
    blocks = []
    nrows, ncols = arr.shape
    for r in range(nrows):
        for c in range(ncols):
            spot = arr[r, c] 
            if spot == '#':
                blocks.append(Border(r, c, verbose=verbose))
            elif spot == 'O':
                blocks.append(Box(r, c, verbose=verbose))
            elif spot == '[':
                last_pos = (r, c)
            elif spot == ']':
                blocks.append(BigBox(*last_pos, r, c, verbose=verbose))

    pos = np.argwhere(arr == '@').flatten()
    return blocks, pos

def solve(map_src: str, moves_src: str, widen=False, verbose=False) -> int:
    if moves_src.endswith('.txt'):
        with open(moves_src, 'r') as f:
            moves_src = f.read()

    G = Grid(*parse(map_src, widen=widen, verbose=verbose), verbose=verbose)
    if verbose:
        print(G)
    G.apply_moves(moves_src)    
    return G.score()


# Tests

given_map = \
"""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########"""

given_moves = \
"""<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

def test_part_1():
    assert solve(given_map, given_moves) == 10092

def test_part_2():
    assert solve(given_map, given_moves, widen=True) == 9021