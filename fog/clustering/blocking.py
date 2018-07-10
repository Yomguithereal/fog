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
from fog.clustering.utils import make_similarity_function

# TODO: max_block_size to avoid ngrams with high DF


def blocking_worker(payload):
    """
    Worker function used compute pairwise distance/similarity over a whole
    block.

    """
    similarity, block, serialized, graph = payload

    if serialized:
        similarity = dill.loads(similarity)

    matches = []
    n = len(block)

    for i in range(n):
        A = block[i]

        for j in range(i + 1, n):
            B = block[j]

            if graph is not None and A in graph and B in graph[A]:
                continue

            if similarity(A, B):
                matches.append((A, B))

    return matches


def blocking(data, block=None, blocks=None, similarity=None, distance=None,
             radius=None, min_size=2, max_size=float('inf'), processes=1):
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

    # Fuzzy clustering
    if processes == 1:
        for bucket in buckets.values():
            if len(bucket) < 2:
                continue

            if type(bucket) is not list:
                bucket = list(bucket)

            for A, B in blocking_worker((similarity, bucket, False, worker_graph)):
                add(graph[A], B)
                add(graph[B], A)
    else:

        pickled_similarity = dill.dumps(similarity)

        pool_iter = (
            (pickled_similarity, bucket if type(bucket) is list else list(bucket), True, None)
            for bucket
            in buckets.values()
            if len(bucket) > 1
        )

        with Pool(processes=processes) as pool:
            for matches in pool.imap_unordered(blocking_worker, pool_iter):
                for A, B in matches:
                    add(graph[A], B)
                    add(graph[B], A)

    # Building clusters
    visited = set()
    for A, neighbors in graph.items():
        if A in visited:
            continue

        if len(neighbors) + 1 < min_size:
            continue
        if len(neighbors) + 1 > max_size:
            continue

        visited.update(neighbors)

        cluster = [A] + (neighbors if type(neighbors) is list else list(neighbors))
        yield cluster
