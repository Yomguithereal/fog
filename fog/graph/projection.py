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

MONOPARTITE_PROJECTION_METRICS = ('cosine', 'jaccard', 'overlap')


def monopartite_projection(bipartite, project, part='bipartite', weight='weight',
                           metric=None, threshold=None):
    """
    Function computing a monopartite projection of the given bipartite graph and
    filtering potential edges by using a similarity metric.

    Args:
        bipartite (nx.Graph): Target bipartite graph. The function will raise an
            error in case the given graph is not truly bipartite.
        project (str): Name of the partition to project.
        part (str, optional): Name of the partition attribute.
            Defaults to "bipartite" wrt networkx conventions.
        weight (str, optional): Name of the weight attribute.
            Defaults to "weight" wrt networkx conventions.
        metric (str, optional): Metric to use. If `None`, the basic projection
            will be returned. Also accepts `jaccard`, `overlap` or `cosine`.
            Defaults to basic projection.
        threshold (float, optional): Optional similarity threshold under which
            edges won't be added. Defaults to no threshold.

    Returns:
        nx.Graph: The monopartite projection.

    """

    if metric is not None and metric not in MONOPARTITE_PROJECTION_METRICS:
        raise TypeError('fog.graph.monopartite_projection: unsupported metric "%s"' % metric)

    if metric != 'cosine' and metric is not None:
        raise NotImplementedError

    monopartite = nx.Graph()

    # Initialising monopartite graph
    for node, attr in bipartite.nodes(data=True):
        if attr[part] != project:
            continue

        monopartite.add_node(node, **attr)

    # Basic projection
    if metric is None:

        for n1 in monopartite.nodes:
            for _, np in bipartite.edges(n1):
                for _, n2 in bipartite.edges(np):

                    # Undirectedness
                    if n1 >= n2:
                        continue

                    if monopartite.has_edge(n1, n2):
                        monopartite[n1][n2][weight] += 1
                    else:
                        monopartite.add_edge(n1, n2, **{weight: 1})

        return monopartite

    # Accumulating norms
    # TODO: we could try to save up the vectors memory cost by relying on graph
    norms = {}
    vectors = {}

    for node in monopartite.nodes:
        s = 0
        neighbors = {}

        for _, neighbor, w in bipartite.edges(node, data=weight, default=1):
            if metric == 'cosine':
                s += w * w
            else:
                s += 1

            neighbors[neighbor] = w

        if s > 0:
            if metric == 'cosine':
                norms[node] = math.sqrt(s)
            else:
                norms[node] = s

            vectors[node] = neighbors

    nodes = list(norms.keys())

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
                monopartite.add_edge(n1, n2, **{weight: w})

    return monopartite
