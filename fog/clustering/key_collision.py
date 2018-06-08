# =============================================================================
# Fog Key Collision Clustering
# =============================================================================
#
# Clustering algorithm grouping items by key collision.
#
from collections import defaultdict


def key_collision(data, key=None, keys=None, min_size=2, max_size=float('inf'),
                  merge=False):
    """
    Function returning an iterator over found clusters.

    It works by grouping items in buckets if they share the same key, as
    returned by a key function. Useful key functions that can efficiently
    regroup similar strings range from case normalization to phonetic encodings
    to clever fingerprint functions such as the one used by OpenRefine.

    Since it runs in O(n), it is one of the fastest record-linkage clustering
    algorithm. However, it won't be able to match more subtle string
    differences such as typos etc.

    Note that the key function can return more than one key for the string.
    In that case, buckets can be merged or not and produce slightly different
    clusters.

    Note also that falsey key are dropped.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        key (callable): A function returning an item's key.
        keys (callable): A function returning an item's keys.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.
        merge (bool, optional): whether to merge the buckets to form clusters.

    Yield:
        list: A viable cluster.

    """

    buckets = defaultdict(list)

    # Single key
    if key is not None:
        for item in data:
            k = key(item)

            if k:
                buckets[k].append(item)

    # Multiple keys
    elif keys is not None:
        for item in data:
            ks = keys(item)

            for k in ks:
                if k:
                    buckets[k].append(item)

    # Merging clusters
    if merge:
        graph = defaultdict(set)

        for bucket in buckets.values():
            n = len(bucket)

            for i in range(n):
                A = bucket[i]

                for j in range(i + 1, n):
                    B = bucket[j]

                    graph[A].add(B)
                    graph[B].add(A)

        visited = set()

        for item, neighbors in graph.items():
            if item in visited:
                continue

            if len(neighbors) + 1 < min_size:
                continue
            if len(neighbors) + 1 > max_size:
                continue

            visited.update(neighbors)

            cluster = [item] + list(neighbors)
            yield cluster

    # Buckets as clusters
    else:
        for cluster in buckets.values():
            if len(cluster) < min_size or len(cluster) > max_size:
                continue
            yield cluster
