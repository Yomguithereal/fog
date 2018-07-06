# =============================================================================
# Fog Sorted Neighborhood Clustering
# =============================================================================
#
# Implementation of the Sorted Neighborhood method.
#
from collections import defaultdict
from fog.clustering.utils import make_similarity_function


def sorted_neighborhood(data, key=None, similarity=None, distance=None,
                        radius=None, window=10, min_size=2, max_size=float('inf')):
    """
    Function returning an iterator over found clusters using the sorted
    neighborhood method.

    It works by first sorting the data according to a key which could, if
    cleverly chosen, put similar items next to one another in the result.

    We then attempt to find clusters by computing pairwise similarity/distances
    in small blocks of constant size in the sorted list.

    Omission key & skeleton keys by Pollock & Zamora are a good choice of
    sorting key if you try to find mispellings, for instance.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        key (callable, optional): key on which to sort the data.
        similarity (callable): If radius is specified, a function returning
            the similarity between two points. Else, a function returning
            whether two points should be deemed similar. Alternatively, one can
            specify `distance` instead.
        distance (callable): If radius is specified, a function returning
            the distance between two points. Else, a function returning
            whether two point should not be deemed similar. Alternatively, one
            can specify `similarity` instead.
        radius (number, optional): produced clusters' radius.
        window (number, optional): Size of the window in which to look for
            matches. Defaults to 10.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.

    Yields:
        list: A viable cluster.

    """

    # Formatting similarity
    similarity = make_similarity_function(similarity=similarity, distance=distance, radius=radius)

    # Iterating over sorted data
    S = sorted(data, key=key)
    n = len(S)

    graph = defaultdict(list)

    for i in range(n):
        A = S[i]

        for j in range(i + 1, min(n, i + window + 1)):
            B = S[j]

            if similarity(A, B):
                graph[i].append(j)
                graph[j].append(i)

    # Building clusters
    visited = set()
    for i, neighbors in graph.items():
        if i in visited:
            continue

        if len(neighbors) + 1 < min_size:
            continue
        if len(neighbors) + 1 > max_size:
            continue

        visited.update(neighbors)

        cluster = [S[i]] + [S[j] for j in neighbors]
        yield cluster
