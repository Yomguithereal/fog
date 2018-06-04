# =============================================================================
# Fog Pairwise Clustering
# =============================================================================
#
# Clustering algorithm computing every pairwise distance/similarity to find
# suitable matches.
#
from collections import defaultdict
from phylactery import BitSet
from fog.clustering.utils import make_similarity_function

# TODO: use a bitset
# TODO: better docs & explanation


def pairwise(data, similarity=None, distance=None, radius=None,
             min_size=2, max_size=float('inf')):
    """
    Function returning an iterator over found clusters using a naive
    algorithm computing every pairwise distance/similarity calculations
    to find matches.

    Runs in O(n * (n - 1) / 2), i.e. O(n^2).

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
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

    Yields:
        list: A viable cluster.

    """

    # Formatting similarity
    similarity = make_similarity_function(similarity=similarity, distance=distance, radius=radius)

    # We need to consume as a list to be able of random access
    if type(data) is not list:
        data = list(data)

    n = len(data)
    visited = BitSet(n)

    for i in range(n):
        A = data[i]

        if i in visited:
            continue

        cluster = None

        for j in range(i + 1, n):
            B = data[j]

            if similarity(A, B):

                if cluster is None:
                    cluster = [A, B]
                else:
                    cluster.append(B)

                if len(cluster) > max_size:
                    for i in range(1, len(cluster)):
                        visited.reset(i)
                    break

                visited.add(j)

        if cluster is not None and len(cluster) >= min_size:
            yield cluster


def fuzzy_pairwise(data, similarity=None, distance=None, radius=None,
                   min_size=2, max_size=float('inf')):
    """
    Function returning an iterator over found clusters using a naive
    algorithm computing every pairwise distance/similarity calculations
    to find matches.

    Runs in O(n * (n - 1) / 2), i.e. O(n^2).

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
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

    Yields:
        list: A viable cluster.

    """

    # Formatting similarity
    similarity = make_similarity_function(similarity=similarity, distance=distance, radius=radius)

    # We need to consume as a list to be able of random access
    if type(data) is not list:
        data = list(data)

    n = len(data)
    graph = defaultdict(list)

    # Computing similarities
    for i in range(n):
        A = data[i]

        for j in range(i + 1, n):
            B = data[j]

            if similarity(A, B):
                graph[i].append(j)
                graph[j].append(i)

    # Building clusters
    visited = BitSet(n)
    for i, neighbors in graph.items():
        if i in visited:
            continue

        if len(neighbors) + 1 < min_size:
            continue
        if len(neighbors) + 1 > max_size:
            continue

        visited.update(neighbors)

        cluster = [data[i]] + [data[j] for j in neighbors]
        yield cluster
