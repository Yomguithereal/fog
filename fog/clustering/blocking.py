# =============================================================================
# Fog Blocking Clustering
# =============================================================================
#
# Implementation of a blocking clusterer that starts by dispatching given
# items to one or more buckets before computing pairwise comparisons on them.
#
import dill
from collections import defaultdict
from multiprocessing import Pool
from fog.clustering.utils import make_similarity_function, clusters_from_pairs

# TODO: max_block_size to avoid ngrams with high DF
# TODO: worker using a VPTree
# TODO: custom inner algorithm
# TODO: fuzzy blocking variant
# TODO: possibility not to merge if sure cannot collide twice
# TODO: the worker_graph is not used right now, the code does not use it (make a clusters from graph also)


def block_worker(payload):
    """
    Worker function used compute pairwise distance/similarity over a whole
    block.

    """
    similarity, block, serialized, graph = payload

    if serialized:
        similarity = dill.loads(similarity)

    pairs = []
    n = len(block)

    for i in range(n):
        A = block[i]

        for j in range(i + 1, n):
            B = block[j]

            if graph is not None and A in graph and B in graph[A]:
                continue

            if similarity(A, B):
                pairs.append((A, B))

    return pairs


def blocking(data, block=None, blocks=None, similarity=None, distance=None,
             radius=None, min_size=2, max_size=float('inf'), processes=1,
             mode='connected_components'):
    """
    Function returning an iterator over found clusters using the blocking
    method.

    It works by dispatching given items into one or more buckets before
    computing pairwise comparisons on each bucket.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        block (callable): A function returning an item's block.
        blocks (callable): A function returning an item's blocks.
        similarity (callable): If radius is specified, a function returning
            the similarity between two points. Else, a function returning
            whether two points should be deemed similar. Alternatively, one can
            specify `distance` instead.
        distance (callable): If radius is specified, a function returning
            the distance between two points. Else, a function returning
            whether two point should not be deemed similar. Alternatively, one
            can specify `similarity` instead.
        radius (number, optional): produced clusters' radius.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.
        processes (number, optional): number of processes to use.
            Defaults to 1.
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.

    Yields:
        list: A viable cluster.

    """

    # Formatting similarity
    similarity = make_similarity_function(similarity=similarity, distance=distance, radius=radius)

    # Single block or blocks?
    if blocks is None:
        graph = defaultdict(list)
        worker_graph = None

        def add(x, y):
            x.append(y)
    else:
        graph = defaultdict(set)
        worker_graph = graph

        def add(x, y):
            x.add(y)

    # Grouping items into buckets
    buckets = defaultdict(list)

    for item in data:
        if blocks is None:
            buckets[block(item)].append(item)
        else:
            bs = set(blocks(item))

            for b in bs:
                buckets[b].append(item)

    # Actual clustering
    def clustering():
        if processes == 1:
            for bucket in buckets.values():
                if len(bucket) < 2:
                    continue

                if type(bucket) is not list:
                    bucket = list(bucket)

                yield from block_worker((similarity, bucket, False, worker_graph))
        else:

            pickled_similarity = dill.dumps(similarity)

            pool_iter = (
                (pickled_similarity, bucket if type(bucket) is list else list(bucket), True, None)
                for bucket
                in buckets.values()
                if len(bucket) > 1
            )

            with Pool(processes=processes) as pool:
                for pairs in pool.imap_unordered(block_worker, pool_iter):
                    yield from pairs

    yield from clusters_from_pairs(
        clustering(),
        fuzzy=blocks is not None,
        min_size=min_size,
        max_size=max_size,
        mode=mode
    )
