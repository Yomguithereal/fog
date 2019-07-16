# =============================================================================
# Fog Key Collision Clustering
# =============================================================================
#
# Clustering algorithm grouping items by key collision.
#
# [Url]:
# http://openrefine.org/
#
from collections import defaultdict

from fog.clustering.utils import clusters_from_buckets


def key_collision(data, key=None, keys=None, min_size=2, max_size=float('inf'),
                  merge=True):
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
    clusters. When using multiple keys per item, if the key space is dense, you
    should definitely merge buckets or you will end up with a large number
    of very similar clusters. If key space is sparse, you can avoid merging
    as an optimization strategy.

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
            Defaults to True.

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

            if not ks:
                continue

            for k in ks:
                if k:
                    buckets[k].append(item)

    # Merging clusters
    if merge and key is None:
        yield from clusters_from_buckets(buckets.values(), fuzzy=True)

    # Buckets as clusters
    else:
        for cluster in buckets.values():
            if len(cluster) < min_size or len(cluster) > max_size:
                continue
            yield cluster
