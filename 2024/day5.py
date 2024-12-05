import pandas as pd
import numpy as np
from graphlib import TopologicalSorter
from io import StringIO
from typing import Union


def get_inputs(rules: Union[str, StringIO], lists: Union[str, StringIO], max_len=30) -> tuple[pd.DataFrame]:
    """
    Retrieve inputs from two separate sources:
    - One containing the rules
    - One containing the lists.

    params:
        rules: The rules file
        lists: The lists file
        max_len: Any number >= than the maximum length of any list in lists. 
                 This lets us use `pd.read_csv` with minimal effort. 

    returns:
        - The rules DF, with `before` and `after` columns.
        - The lists DF, with numerical column names. Will contain `NaN`s!
    
    """
    a = pd.read_csv("input/day5a.txt", header=None, sep="|", names=['before', 'after'])
    b = pd.read_csv("input/day5b.txt", header=None, names=range(max_len))
    return a, b


def topological_sort(df: pd.DataFrame) -> TopologicalSorter:
    "Consumes a rules DataFrame and returns a valid topological ordering of the numbers."
    ts = TopologicalSorter()
    for before, after in df.itertuples(index=False):
        ts.add(after, before)
    return tuple(ts.static_order())


def remove_nan(lst: list) -> list:
    """Remove `NaN` values to facilitate working with DataFrames."""
    return [int(x) for x in lst if not np.isnan(x)]


def validate(lst: tuple[int], df: pd.DataFrame) -> bool:
    """
    The critical observation is that a valid list will be in topological order.
    Each number represents a node in a graph, and the provided rules represent the directed edges.
    By traversing this graph, we can generate a valid ordering of nodes,
    which we then compare to the given list.

    Note that we filter the set of rules to only include ones which are relevant to our nodes.
    This is necessary to prevent cycles from forming in the graph.

    params:
        lst: The list to be checked.
        df:  The rules df.

    returns:
        Whether the given list represents a valid ordering according to the rules.
    """
    l = remove_nan(lst)
    rules = df[(df['before'].isin(l)) & (df['after'].isin(l))]
    for item in topological_sort(rules):
        if len(l) > 0 and l[0] == item:
            l.pop(0)
    return len(l) == 0


def fix(lst: list[int], df: pd.DataFrame) -> list[int]:
    """Fixes a list assumed not to be in topological order. Returns the new list."""
    
    l = remove_nan(lst)
    rules = df[(df['before'].isin(l)) & (df['after'].isin(l))]
    return topological_sort(rules)


def middles(lists: list[list[int]]) -> int:
    """Sum the middle elements of a list of lists"""
    return sum([l[int(len(l)/2)] for l in lists])


def solve(df1: pd.DataFrame, df2: pd.DataFrame) -> bool:
    """
    Separates the dataset into valid and invalid lists.
    Fixes invalid lists, then sums the middles of each.

    params:
        df1: The rules DF
        df2: The lists DF

    returns:
        - Part 1 answer
        - Part 2 answer
    """
    valid = [remove_nan(l) for l in df2.itertuples(index=False) if validate(l, df1)]
    invalid = [remove_nan(l) for l in df2.itertuples(index=False) if not validate(l, df1)]
    fixed = [fix(i, df1) for i in invalid]
    return middles(valid), middles(fixed) 


# Tests

given1 = \
"""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13"""

given2 = \
"""75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

def test_both_parts():
    given = get_inputs(StringIO(given1), StringIO(given2))
    assert solve(*given) == (143, 123)