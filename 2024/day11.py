from tqdm.autonotebook import tqdm
from collections import Counter, defaultdict

"""
This puzzle was a little weird... 
The main challenge was beating the explosion of the number of stones if you do it manually.

While there could be millions of stones in the list, there are likely much fewer *unique* stones.
Thus, the solution is to only store one of each stone value, as well as a quantity.
That way we can do the (cached) mutation exactly one per unique value per generation.

Note: I manually copied the puzzle inputs since they were so brief. Sorry.
"""


def delta(stone: int) -> tuple[int]:
    """Apply the changes to a stone. Returns a single or double of the results."""
    s = str(stone)
    if stone == 0:
        return (1,)
    elif len(s) % 2 == 0:
        return int(s[:len(s)//2]), int(s[len(s)//2:])
    else:
        return (stone * 2024,)


def mutate(counts: dict[int, int],  mutations: dict[int, tuple[int]]) -> dict[int, int]:
    """
    Applies the changes to a whole set of stones.

    Params:
        counts: A mapping of stone value to the number of occurrences.
        mutations: A cache of stone values to mutated values.
                   Not sure if this is worth it, but I figured it couldn't hurt to save function calls.

    Returns:
        A new dict resembling `count` for the next generation.
    """
    output = defaultdict(int)
    for stone, num in counts.items():
        res = mutations.get(stone, delta(stone))
        mutations[stone] = res
        for mutated in res:
            output[mutated] += num
            
    return output


def count_stones(stone_dict: dict[int, int]) -> int:
    """Compute the number of stones in a counter."""
    return sum([v for v in stone_dict.values()])


def simulate(stones: list[int], n: int, verbose=False) -> list[int]:
    """How many stones will there be after `n` generations of mutations on the initial list `stones`?"""
    mutations = {} # avoid superflouous function calls
    counts = defaultdict(int, Counter(stones)) # Since the linear order doesn't matter, just store the amounts of each stone.
    for _ in tqdm(range(n)) if verbose else range(n):
        counts = mutate(counts, mutations)
        if verbose:
            print(count_stones(counts))
    return count_stones(counts)


# Tests

given = [120, 17]

def test_part_1():
    assert simulate(given, 25) == 55312

def test_part_2():
    assert simulate(given, 75) == 65601038650482



# Some extras for fun

def simulate_counts(stones: list[int], n: int) -> list[int]:
    """Like simulate, but returns a list of counts after every generation."""
    mutations = {} # avoid superflouous function calls
    counts = defaultdict(int, Counter(stones)) # Since the linear order doesn't matter, just store the amounts of each stone.
    output = [counts]
    for _ in range(n):
        counts = mutate(counts, mutations)
        output.append(counts)
    return output

def plot_stones(stones=(125, 17), n=75):
    x = range(n+1)
    counts = simulate_counts(stones, n)
    totals, uniques = [], []
    for count in counts:
        totals.append(count_stones(count))
        uniques.append(len(count))

    _, ax = plt.subplots()
    ax.plot(x, totals, label='Total Stones')
    ax.plot(x, uniques, label='Unique Stones')
    ax.set_yscale('log')
    ax.set_xlabel('Generation')
    ax.set_ylabel('# Stones')
    ax.set_title('Number of stones by generation')
    ax.legend()
    plt.show()
    