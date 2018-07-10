# =============================================================================
# Fog Vantage Point Tree Clustering
# =============================================================================
#
# Clustering algorithm leveraging a Vantage Point Tree to avoid needing to
# compute pairwise distances. In practice, it means that the number of
# distance computations needed per point will be sublinear. Therefore,
# parallelization of the brute-force algorithm often yields better results.
#
# [Reference]:
# Data Structures and Algorithms for Nearest Neighbor Search in General
# Metric Space. Peter N. Yianilos.
#
from phylactery import VPTree


def vp_tree(data, distance, radius, min_size=2, max_size=float('inf')):
    """
    Function returning an iterator over found clusters.

    It works by indexing given items into a Vantage Point Tree and then
    querying the tree once per items to find clusters.

    It runs in O(n log n * m), m being the number of matches or leaves to
    traverse in the tree when querying. In practice this is lower than
    O(n^2) but will tend towards it as soon as the number of items becomes too
    large (intuitively, this is because the dimensionality of the queried
    space becomes really high and we hit the curse of high-dimensionality).

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        radius (number): produced clusters' radius.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.

    Yield:
        list: A viable cluster.

    """

    if type(data) is not list:
        data = list(data)

    tree = VPTree(data, distance, selection='spread')

    visited = set()

    for item in data:
        if item in visited:
            continue

        cluster = [neighbor for neighbor, _ in tree.neighbors_in_radius(item, radius)]

        # TODO: with max_size we can use the knn version
        if len(cluster) < min_size or len(cluster) > max_size:
            continue

        visited.update(cluster)

        yield cluster
