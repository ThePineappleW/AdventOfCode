#! /usr/bin/env python

import networkx as nx

from utils import AOCrunner

INPUTFILE = r"inputs/day11.txt"
TESTCASE = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

TESTCASE2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


def parse(f) -> nx.DiGraph:
    G = nx.DiGraph()
    for line in f:
        source = line[:3]
        to = line[5:].split()
        for node in to:
            G.add_edge(source, node)
    return G


def count_paths_v1(f, source="you", target="out", verbose=False) -> int:
    """
    Hey, there's a function for that!
    However, this is very slow, since there are O(n!) in a connected graph of order n.
    """
    G = parse(f)
    if verbose:
        (print(G, source, target),)
    return len(list(nx.all_simple_paths(G, source, target)))


def count_paths(G: nx.DiGraph, source: str, target: str, verbose=False):
    """
    Finding all simple paths between two points on a large graph can be very slow.
    Looking at the inputs a little closer, it turns out that they are acyclic.

    This can be verified with
    >>    assert nx.is_directed_acyclic_graph(G)

    Since G is a DAG, we can use topological sort to order the nodes.
    This is very similar to day 7, except that we have to handle
    arbitrary and end nodes.

    The easiest way to to this is just to make a subgraph containing
    only descendents of the start node.
    """
    subgraph = G.subgraph(nx.descendants(G, source) | {source})
    nodes = list(nx.topological_sort(subgraph))

    if verbose:
        print(nodes)

    memo = {source: 1}
    for node in nodes:
        if node == source:
            continue
        memo[node] = sum(memo[parent] for parent in subgraph.predecessors(node))

    if verbose:
        print(memo)
        print()
    return memo.get(target, 0)


def part1_runner(f) -> int:
    return count_paths(parse(f), "you", "out")


def count_paths_through(
    f, source="svr", target="out", thru=("fft", "dac"), verbose=False
) -> int:
    """
    To calculate the number of unique paths that include fft and dac,
    count the number of the following paths:
        1. svr --> fft
        2. fft --> dac
        3. dac --> out
    Since each total path must include one of each section,
    simply multiply the counts together to compute the number of possible paths.

    Note that the "in any order" hint in the problem is a red herring!
    Having paths fft --> dac and dac --> fft would create a cycle.
    """
    G = parse(f)
    leg1 = count_paths(G, source, thru[0], verbose=verbose)
    leg2 = count_paths(G, thru[0], thru[1], verbose=verbose)
    leg3 = count_paths(G, thru[1], target, verbose=verbose)
    if verbose:
        print(f"{source} -{leg1}-> {thru[0]} -{leg2}-> {thru[1]} -{leg3}-> {target}")
    return leg1 * leg2 * leg3


if __name__ == "__main__":
    aoc = AOCrunner(INPUTFILE, TESTCASE, TESTCASE2)
    aoc.part1(part1_runner, 5, verbose=False)
    aoc.part2(count_paths_through, 2, verbose=False)
