# =============================================================================
# Fog Graph Utils
# =============================================================================
#
# Miscellaneous utility functions related to graphs.
#
from heapq import nlargest


def component_sizes(g):
    seen = set()
    stack = []

    for node in g.nodes:

        if node in seen:
            continue

        c = 0
        stack = [node]

        while len(stack) != 0:
            v = stack.pop()

            if v not in seen:
                seen.add(v)
                c += 1
                stack.extend(g.neighbors(v))

        yield c


def second_largest_component_size(g):
    top = nlargest(2, component_sizes(g))

    if len(top) < 2:
        return None

    return top[1]
