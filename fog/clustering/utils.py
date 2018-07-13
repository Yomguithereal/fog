# =============================================================================
# Fog Clustering Utilities
# =============================================================================
#
# Miscellaneous redundant functions used by clustering routines.
#
from collections import defaultdict
import math


def make_similarity_function(similarity=None, distance=None, radius=None):
    """
    Function creating a similarity function returning True if the compared
    items are similar from a variety of functions & parameters.

    Basically, if a distance function is given, it will be inverted and if
    a radius is given, the returned function will return whether the
    distance/similarity between two items is under/over it.

    Args:
        similarity (callable, optional): Similarity function.
        distance (callable, optional): Distance function.
        radius (number, optional): Radius.

    Returns:
        function: A similarity function with signature (A, B) -> bool

    """
    if similarity is None and distance is None:
        raise TypeError('fog.clustering: need at least a similarity or distance function.')

    if radius is not None:
        if similarity:
            return lambda A, B: similarity(A, B) >= radius
        else:
            return lambda A, B: distance(A, B) <= radius
    else:
        if similarity:
            return similarity
        else:
            return lambda A, B: not distance(A, B)


def clusters_from_pairs(pairs, min_size=2, max_size=float('inf'),
                        mode='connected_components', fuzzy=False):
    """
    Function consuming an iterator of similar pairs and merging them
    according to the desired strategy to yield valid clusters.

    Args:
        pairs (iterable): Similar pairs.
        min_size (int, optional): Minimum size of clusters, defaults to 2.
        max_size (int, optional): Maximum size of clusters, defaults to
            infinity.
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.
        fuzzy (bool, optional): whether a same pair can arrive twice or not.
            Defaults to False.

    Yields:
        list: A viable cluster.

    """

    container = set if fuzzy else list

    if fuzzy:
        def add(c, x):
            c.add(x)
    else:
        def add(c, x):
            c.append(x)

    # TODO: later, we'll be able to use SparseSet rather than the graph
    # TODO: in the connected component case, we don't need mutual links
    graph = defaultdict(container)

    for A, B in pairs:
        add(graph[A], B)
        add(graph[B], A)

    if mode == 'fuzzy_clusters':
        visited = set()

        for item, neighbors in graph.items():
            if item in visited:
                continue

            if len(neighbors) + 1 < min_size:
                continue
            if len(neighbors) + 1 > max_size:
                continue

            visited.update(neighbors)

            cluster = [item] + (list(neighbors) if fuzzy else neighbors)
            yield cluster

    elif mode == 'connected_components':
        visited = set()
        stack = []

        for item, neighbors in graph.items():
            if item in visited:
                continue

            visited.add(item)

            cluster = [item]

            stack.extend(neighbors)

            while len(stack) != 0:
                neighbor = stack.pop()

                if neighbor in visited:
                    continue

                cluster.append(neighbor)
                visited.add(neighbor)

                stack.extend(graph[neighbor])

            if len(cluster) >= min_size and len(cluster) <= max_size:
                yield cluster

    else:
        raise TypeError('fog.clustering: unknown mode "%s"' % mode)


def pairs_from_buckets(buckets):
    """
    Function yielding similarity pairs from buckets.

    """
    for bucket in buckets:
        n = len(bucket)

        for i in range(n):
            A = bucket[i]

            for j in range(i + 1, n):
                B = bucket[j]

                yield (A, B)


def clusters_from_buckets(buckets, min_size=2, max_size=float('inf'),
                          mode='connected_components', similarity=None,
                          fuzzy=False):
    """
    Function merging buckets into fuzzy clusters. Each bucket will create
    relations in an undirected graph that is later solved to compose clusters.

    Args:
        buckets (iterable): Buckets to merge.
        min_size (int, optional): Minimum size of clusters, defaults to 2.
        max_size (int, optional): Maximum size of clusters, defaults to
            infinity.
        mode (string, optional): 'fuzzy_clusters', 'connected_components' or
            'leader'. Defaults to 'connected_components'.
        similarity (callable, optional)= similarity function to use to validate
            matches from buckets.
        fuzzy (bool, optional): whether a same pair can arrive twice or not.
            Defaults to False.

    Yields:
        list: A viable cluster.

    """

    pairs = (
        pair
        for pair
        in pairs_from_buckets(buckets)
        if similarity is None or similarity(pair[0], pair[1])
    )

    yield from clusters_from_pairs(
        pairs,
        min_size=min_size,
        max_size=max_size,
        mode=mode,
        fuzzy=fuzzy
    )


def upper_triangular_matrix_chunk_iter(data, chunk_size):
    """
    Function returning an iterator over chunks of an upper triangular matrix.
    It's a useful utility to parallelize pairwise distance computations, for
    instance.

    Args:
        data (iterable): The matrix's data.
        chunk_size (int): Size of the chunks to yield.

    Yields:
        tuple of slices: A matrix's chunk.

    """
    n = len(data)
    c = math.ceil(n / chunk_size)

    for j in range(c):
        j_offset = j * chunk_size
        j_limit = j_offset + chunk_size

        for i in range(0, min(j + 1, c)):
            i_offset = i * chunk_size
            i_limit = i_offset + chunk_size

            yield (
                data[i_offset:i_limit],
                data[j_offset:j_limit] if i_offset != j_offset else [],
                i_offset,
                j_offset
            )
