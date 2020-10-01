# =============================================================================
# Fog Graph Projections
# =============================================================================
#
# Miscellaneous functions related to bipartite to monopartite projections.
#
import math
import networkx as nx
from collections import defaultdict, Counter

from fog.metrics import sparse_dot_product


def cosine_monopartite_projection(bipartite, keep, part='bipartite', weight='weight',
                                  threshold=None):
    monopartite = nx.Graph()

    vectors = defaultdict(Counter)

    # TODO: what to do with nodes having no edges?
    for n1, n2, w in bipartite.edges(data=weight, default=1):
        p1 = bipartite.nodes[n1][part]
        p2 = bipartite.nodes[n2][part]

        assert p1 != p2, 'fog.graph.cosine_monopartite_projection: given graph is not truly bipartite.'

        # Swapping so n1 is from part to keep
        if p2 == keep:
            n1, n2 = n2, n1

        vectors[n1][n2] += w

    norms = {}
    nodes = list(vectors)
    # inverted_index = defaultdict(list)

    for node, vector in vectors.items():
        monopartite.add_node(node, **bipartite.nodes[node])
        s = 0

        for neighbor, w in vector.items():
            s += w * w
            # inverted_index[neighbor].append(node)

        norms[node] = math.sqrt(s)

    # Quadratic version
    l = len(nodes)

    for i, n1 in enumerate(nodes):
        norm1 = norms[n1]
        vector1 = vectors[n1]

        for j in range(i + 1, l):
            n2 = nodes[j]
            norm2 = norms[n2]
            vector2 = vectors[n2]

            w = sparse_dot_product(vector1, vector2)

            if w == 0:
                continue

            # NOTE: at this point, both norms should be > 0, so no need to test
            w = w / (norm1 * norm2)

            if threshold is None or w >= threshold:
                monopartite.add_edge(n1, n2, weight=w)

    return monopartite
