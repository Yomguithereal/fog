# =============================================================================
# Fog Graph Projections
# =============================================================================
#
# Miscellaneous functions related to bipartite to monopartite projections.
#
import math
import networkx as nx
from collections import defaultdict, Counter

from fog.metrics.cosine import sparse_dot_product
from fog.metrics.utils import intersection_size

MONOPARTITE_PROJECTION_METRICS = ('cosine', 'jaccard', 'overlap')
EMPTY_COUPLE = (None, None)


def compute_metric(metric, vector1, vector2, norm1, norm2):
    if metric == 'cosine':
        w = sparse_dot_product(vector1, vector2)

        if w == 0:
            return 0

        return w / (norm1 * norm2)

    w = intersection_size(vector1, vector2)

    if w == 0:
        return 0

    if metric == 'jaccard':
        return w / (norm1 + norm2 - w)

    if metric == 'overlap':
        return w / min(norm1, norm2)

    raise NotImplementedError


# TODO: use passjoin prefix filtering as optimization scheme
def monopartite_projection(bipartite, project, part='bipartite', weight='weight',
                           metric=None, threshold=None, use_index=False):
    """
    Function computing a monopartite projection of the given bipartite graph.
    This projection can be basic and create a weighted edge each time two nodes
    in target partition share a common neighbor. Or it can be weighted and
    filtered using a similarity metric such as Jaccard or cosine similarity,
    for instance.

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
        use_index (bool, optional): Whether to use indexation techniques to
            attempt a subquadratic time for the projection. This can consume
            a lot of memory depending on your dataset. But if you can guarantee
            that the probability that two nodes share the same neighbor is low,
            then it can drastically improve your performance.

    Returns:
        nx.Graph: The monopartite projection.

    """

    if metric is not None and metric not in MONOPARTITE_PROJECTION_METRICS:
        raise TypeError('fog.graph.monopartite_projection: unsupported metric "%s"' % metric)

    monopartite = nx.Graph()

    # Initialising monopartite graph
    for node, attr in bipartite.nodes(data=True):
        if attr[part] != project:
            continue

        monopartite.add_node(node, **attr)

    # Accumulating norms
    # TODO: we could try to save up the vectors memory cost by relying on graph
    vectors = {}

    if metric is not None:
        for node in monopartite.nodes:
            s = 0
            neighbors = {} if metric == 'cosine' else set()

            for _, neighbor, w in bipartite.edges(node, data=weight, default=1):
                if metric == 'cosine':
                    s += w * w
                    neighbors[neighbor] = w
                else:
                    s += 1
                    neighbors.add(neighbor)

            if s > 0:
                if metric == 'cosine':
                    vectors[node] = (math.sqrt(s), neighbors)
                else:
                    vectors[node] = (s, neighbors)

    # Basic projection
    if metric is None or use_index:

        for n1 in monopartite.nodes:
            norm1, vector1 = vectors.get(n1, EMPTY_COUPLE) if metric is not None else EMPTY_COUPLE

            for _, np in bipartite.edges(n1):
                for _, n2 in bipartite.edges(np):

                    # Undirectedness
                    if n1 >= n2:
                        continue

                    if metric is not None:
                        if monopartite.has_edge(n1, n2):
                            continue

                        norm2, vector2 = vectors[n2]

                        # NOTE: at this point, both norms should be > 0
                        w = compute_metric(metric, vector1, vector2, norm1, norm2)

                        if w == 0:
                            continue

                        monopartite.add_edge(n1, n2, **{weight: w})
                    else:
                        if monopartite.has_edge(n1, n2):
                            monopartite[n1][n2][weight] += 1
                        else:
                            monopartite.add_edge(n1, n2, **{weight: 1})

                    if threshold is not None and w < threshold:
                        continue

        return monopartite

    # Quadratic version
    nodes = list(vectors.keys())
    l = len(nodes)

    for i, n1 in enumerate(nodes):
        norm1, vector1 = vectors[n1]

        for j in range(i + 1, l):
            n2 = nodes[j]
            norm2, vector2 = vectors[n2]

            # NOTE: at this point, both norms should be > 0
            w = compute_metric(metric, vector1, vector2, norm1, norm2)

            if w == 0:
                continue

            if threshold is None or w >= threshold:
                monopartite.add_edge(n1, n2, **{weight: w})

    return monopartite
