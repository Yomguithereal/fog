# =============================================================================
# Fog Vantage Point Tree Clustering
# =============================================================================
#
# Clustering algorithm leveraging a Vantage Point Tree to find suitable
# clusters.
#
from phylactery import VPTree

# TODO: better docs


def vp_tree(data, distance, radius, min_size=2, max_size=float('inf')):
    """
    Function returning an iterator over found clusters.

    It works by leveraging a Vantage point tree and returning, for each
    point not yet in a cluster, the set of its neighbors sitting in a
    given range.

    It runs in O(n log n).

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

    tree = VPTree(data, distance)

    visited = set()

    for item in data:
        if item in visited:
            continue

        cluster = [neighbor for neighbor, _ in tree.neighbors_in_radius(item, radius)]

        if len(cluster) < min_size or len(cluster) > max_size:
            continue

        visited.update(cluster)

        yield cluster
