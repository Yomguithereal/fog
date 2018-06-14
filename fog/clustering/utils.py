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

    if radius:
        if similarity:
            return lambda A, B: similarity(A, B) >= radius
        else:
            return lambda A, B: distance(A, B) <= radius
    else:
        if similarity:
            return similarity
        else:
            return lambda A, B: not distance(A, B)


def merge_buckets_into_clusters(buckets, min_size=2, max_size=float('inf')):
    """
    Function merging buckets into fuzzy clusters. Each bucket will create
    relations in an undirected graph that is later solved to compose clusters.

    Args:
        buckets (iterable): Buckets to merge.
        min_size (int, optional): Minimum size of clusters, defaults to 2.
        max_size (int, optional): Maximum size of clusters, defaults to
            infinity.

    Yields:
        list: A viable cluster.

    """
    graph = defaultdict(set)

    for bucket in buckets:
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
