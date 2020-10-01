# =============================================================================
# Fog Graph Utils
# =============================================================================
#
# Miscellaneous utility functions related to graphs.
#


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
