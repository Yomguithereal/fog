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
                           metric=None, threshold=None, use_topology=True,
                           bipartition_check=True):
    """
    Function computing a monopartite projection of the given bipartite graph.
    This projection can be basic and create a weighted edge each time two nodes
    in target partition share a common neighbor. Or it can be weighted and
    filtered using a similarity metric such as Jaccard or cosine similarity,
    for instance.

    Args:
        bipartite (nx.Graph): Target bipartite graph.
        project (str): Name of the partition to project.
        part (str, optional): Name of the node attribute on which the
            graph partition is built e.g. "color" or "type" etc.
            Defaults to "bipartite" wrt networkx conventions.
        weight (str, optional): Name of the weight edge attribute.
            Defaults to "weight" wrt networkx conventions.
        metric (str, optional): Metric to use. If `None`, the basic projection
            will be returned. Also accepts `jaccard`, `overlap` or `cosine`.
            Defaults to basic projection.
        threshold (float, optional): Optional similarity threshold under which
            edges won't be added to the monopartite projection.
            Defaults to no threshold.
        use_topology (bool, optional): Whether to use the bipartite graph's
            topology to attempt a subquadratic time projection. Intuitively,
            this works by not computing similarities of all pairs of nodes but
            only of pairs of nodes that share at least a common neighbor.
            It generally works better than the quadratic approach but can
            sometimes hurt your performance by losing time on graph traversals
            when your graph is very dense.
        bipartition_check (bool, optional): This function will start by checking
            whether your graph is bipartite because it can get stuck in an
            infinite loop if given graph is not truly bipartite. Be sure to
            disable this kwarg if you know beforehand that your graph is
            bipartite and for better performance.

    Returns:
        nx.Graph: The monopartite projection.

    """

    if metric is not None and metric not in MONOPARTITE_PROJECTION_METRICS:
        raise TypeError('fog.graph.monopartite_projection: unsupported metric "%s"' % metric)

    if bipartition_check:
        parts = set()

        for n1, n2 in bipartite.edges:
            p1 = bipartite.nodes[n1][part]
            p2 = bipartite.nodes[n2][part]

            parts.add(p1)
            parts.add(p2)

            if p1 == p2 or len(parts) > 2:
                raise TypeError('fog.graph.monopartite_projection: given graph is not truly bipartite!')

    monopartite = nx.Graph()

    # Initialising monopartite graph
    for node, attr in bipartite.nodes(data=True):
        if attr[part] != project:
            continue

        monopartite.add_node(node, **attr)

    # Accumulating vectors & norms
    # TODO: we could save up some memory by relying on nx's graph directly
    # But this would make code a bit more complex and won't ease up adapting
    # the function to a sparse vector input
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
    if metric is None or use_topology:

        for n1 in monopartite.nodes:
            norm1, vector1 = vectors.get(n1, EMPTY_COUPLE) if metric is not None else EMPTY_COUPLE

            for np in bipartite.neighbors(n1):
                for n2 in bipartite.neighbors(np):

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

                        if threshold is not None and w < threshold:
                            continue

                        monopartite.add_edge(n1, n2, **{weight: w})
                    else:
                        if monopartite.has_edge(n1, n2):
                            monopartite[n1][n2][weight] += 1
                        else:
                            monopartite.add_edge(n1, n2, **{weight: 1})

        return monopartite

    # Quadratic version
    nodes = list(vectors.items())
    l = len(nodes)

    for i, (n1, (norm1, vector1)) in enumerate(nodes):
        for j in range(i + 1, l):
            (n2, (norm2, vector2)) = nodes[j]

            # NOTE: at this point, both norms should be > 0
            w = compute_metric(metric, vector1, vector2, norm1, norm2)

            if w == 0:
                continue

            if threshold is None or w >= threshold:
                monopartite.add_edge(n1, n2, **{weight: w})

    return monopartite
