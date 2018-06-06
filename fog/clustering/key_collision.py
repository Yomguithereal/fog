# =============================================================================
# Fog Key Collision Clustering
# =============================================================================
#
# Clustering algorithm grouping items by key collision.
#
from collections import defaultdict

# TODO: multiple keys per item


def key_collision(data, key, min_size=2, max_size=float('inf')):
    """
    Function returning an iterator over found clusters.

    It works by grouping the given items by keys in a multimap.

    It therefore runs in O(n).

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        key (callable): A function returning an item's key.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.

    Yield:
        list: A viable cluster.

    """

    clusters = defaultdict(list)

    for item in data:
        k = key(item)

        if k:
            clusters[k].append(item)

    for cluster in clusters.values():
        if len(cluster) < min_size or len(cluster) > max_size:
            continue
        yield cluster
