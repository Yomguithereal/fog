# =============================================================================
# Fog Graph Sparsification
# =============================================================================
#
# Sparsification schemes for networks.
#
import math
from fog.graph.utils import second_largest_component_size


def floatsam_sparsification(graph, starting_treshold=0.0, learning_rate=0.05,
                            max_drifter_size=None, weight='weight',
                            remove_edges=False):
    """
    Function using an iterative algorithm to try and find the best weight
    threshold to apply to trim the given graph's edges while keeping the
    underlying community structures.

    It works by iteratively increasing the threshold and stopping as soon as
    a significant connected component starts to drift away from the principal
    one.

    This is basically a very naive gradient descent with a very naive cost
    function but it works decently for typical cases.

    Args:
        graph (nx.Graph): Graph to sparsify.
        starting_treshold (float, optional): Starting similarity threshold.
            Defaults to `0.0`.
        learning_rate (float, optional): How much to increase the threshold
            at each step of the algorithm. Defaults to `0.05`.
        max_drifter_size (int, optional): Max size of component to detach itself
            from the principal one before stopping the algorithm. If not
            provided it will default to the logarithm of the graph's total
            number of nodes.
        weight (str, optional): Name of the weight attribute.
            Defaults to "weight" wrt networkx conventions.
        remove_edges (bool, optional): Whether to remove edges from the graph
            having a weight less than found threshold or not. Note that if
            `True`, this will mutate the given graph. Defaults to `False`.

    Returns:
        float: The found threshold

    """
    if graph.size() == 0:
        return starting_treshold

    threshold = starting_treshold
    best_threshold = None

    def edge_filter(u, v, attr):
        return attr[weight] >= threshold

    if max_drifter_size is None:
        max_drifter_size = int(math.log(len(graph)))

    while True:
        best_threshold = threshold
        threshold += learning_rate

        c = second_largest_component_size(graph, edge_filter)

        if c is not None and c >= max_drifter_size:
            break

    if remove_edges:
        to_remove = []
        for u, v, w in graph.edges(data=weight):
            if w < best_threshold:
                to_remove.append((u, v))

        for u, v in to_remove:
            graph.remove_edge(u, v)

    return best_threshold
