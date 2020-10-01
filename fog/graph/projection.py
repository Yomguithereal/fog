# =============================================================================
# Fog Graph Projections
# =============================================================================
#
# Miscellaneous functions related to bipartite to monopartite projections.
#
from collections import defaultdict, Counter
from networkx import Graph


def cosine_monopartite_projection(bipartite, keep, part='bipartite', weight='weight',
                                  threshold=None):
    monopartite = Graph()

    vectors = defaultdict(Counter)

    for n1, n2, w in bipartite.edges(data=weight, default=1):
        p1 = bipartite.nodes[n1][part]
        p2 = bipartite.nodes[n2][part]

        assert p1 != p2, 'fog.graph.cosine_monopartite_projection: given graph is not truly bipartite.'

        # Swapping so n1 is from part to keep
        if p2 == part:
            n1, n2 = n2, n1

        vectors[n1][n2] += w

    norms = {}

    for node, vector in vectors.items():
        monopartite.add_node(node, bipartite.nodes[node])
        norms[node] = sum(vector.values())
