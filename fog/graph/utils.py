# =============================================================================
# Fog Graph Utils
# =============================================================================
#
# Miscellaneous utility functions related to graphs.
#
from heapq import nlargest


def component_sizes(g, edge_filter=None):
    seen = set()
    stack = []

    for node in g.nodes:

        if node in seen:
            continue

        c = 0
        stack.append(node)

        while len(stack) != 0:
            n1 = stack.pop()

            if n1 not in seen:
                seen.add(n1)
                c += 1

                for _, n2, edge_attr in g.edges(n1, data=True):
                    if callable(edge_filter) and not edge_filter(n1, n2, edge_attr):
                        continue
                    stack.append(n2)

        yield c


def second_largest_component_size(g, edge_filter=None):
    top = nlargest(2, component_sizes(g, edge_filter))

    if len(top) < 2:
        return None

    return top[1]
