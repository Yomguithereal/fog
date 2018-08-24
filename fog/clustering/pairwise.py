# =============================================================================
# Fog Pairwise Clustering
# =============================================================================
#
# Clustering algorithms computing every pairwise distance/similarity to build
# suitable clusters.
#
import dill
from collections import defaultdict
from multiprocessing import Pool
from phylactery import UnionFind

from fog.clustering.utils import (
    make_similarity_function,
    upper_triangular_matrix_chunk_iter
)


def pairwise_leader(data, similarity=None, distance=None, radius=None,
                    min_size=2, max_size=float('inf')):
    """
    Function returning an iterator over found clusters using the leader
    algorithm.

    It works by assuming the similarity relation is transitive, meaning that
    (A =~ B, B =~ C) leads to A =~ C, which is often quite correct.

    Under the hood, each point will start in its own cluster and each time
    two points are deemed similar, they are merged into the same cluster. Then,
    the first item of the cluster, its leader if you will, is the only one
    that will be used in subsequent similarity comparisons.

    This means three things:
        1) The radius of the produced clusters is sound.
        2) The items' order can have an arbitrary influence on the produced
           clusters.
        3) One item CANNOT belong to more than one cluster.

    This algorithm runs in O(n * (c - 1) / 2), n being the number of items and c
    being the number of clusters, i.e. O(n^2) in practice since for record
    linkage most items will be alone in their clusters.

    Note that this algorithm can work by storing only the current cluster in
    memory.

    Example:
        The following chain:
            ('abc', 'bcd', 'cde', 'def', 'efg', 'ghi')
        will produce the following levenshtein radius=2 clusters:
            ('abc', 'bcd')
            ('cde', 'def')
            ('efg', 'ghi')

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
    visited = set()

    for i in range(n):
        if i in visited:
            continue

        A = data[i]

        cluster = None

        for j in range(i + 1, n):
            if j in visited:
                continue

            B = data[j]

            if similarity(A, B):

                if cluster is None:
                    cluster = [A, B]
                else:
                    cluster.append(B)

                if len(cluster) > max_size:
                    for c in range(1, len(cluster)):
                        visited.delete(c)
                    break

                visited.add(j)

        if cluster is not None and len(cluster) >= min_size:
            yield cluster


def pairwise_worker(payload):
    """
    Worker function used to compute pairwise computations over chunks of
    an upper triangular matrix in parallel.

    """
    similarity, I, J, offset_i, offset_j = payload

    similarity = dill.loads(similarity)
    pairs = []

    diagonal_chunk = offset_i == offset_j

    if diagonal_chunk:
        J = I

    for i in range(len(I)):
        A = I[i]

        for j in range(0 if not diagonal_chunk else i + 1, len(J)):
            B = J[j]

            if similarity(A, B):
                pairs.append((offset_i + i, offset_j + j))

    return pairs


def pairwise_fuzzy_clusters(data, similarity=None, distance=None, radius=None,
                            min_size=2, max_size=float('inf'), key=None,
                            processes=1, chunk_size=100):
    """
    Function returning an iterator over found clusters using an algorithm
    yielding fuzzy clusters.

    This algorithm is a compromise between the "leader" method and the
    "connected components" one in that it won't produce clusters with a radius
    larger that what's expected and will not attempt to cut clusters too
    arbitrarily. To achieve that, this algorithm will yield fuzzy clusters.

    This means three things:
        1) The radius of the produced clusters is sound.
        2) The items' order can have an arbitrary influence on the produced
           clusters.
        3) One item CAN belong to more than one cluster

    This algorithm runs in O(n * (n - 1) / 2), i.e. O(n^2).

    Note that this algorithm can be parallelized and then run in
    O (n * (n - 1) / 2 / p), p being the number of processes.

    TODO: option to sort by degree

    Example:
        The following chain:
            ('abc', 'bcd', 'cde', 'def', 'efg', 'ghi')
        will produce the following levenshtein radius=2 clusters:
            ('abc', 'bcd')
            ('cde', 'bcd', 'def')
            ('efg', 'def', 'fgh')
            ('ghi', 'fgh')

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
        key (callable, optional): function returning an item's key.
            Defaults to None.
        processes (number, optional): number of processes to use. Defaults to 1.
        chunk_size (number, optional): size of matrix chunks to send to
            subprocesses. Defaults to 100.

    Yields:
        list: A viable cluster.

    """

    # Formatting similarity
    similarity = make_similarity_function(similarity=similarity, distance=distance, radius=radius)

    # We need to consume as a list to be able of random access
    if type(data) is not list:
        data = list(data)

    if key is not None:
        keys = list(key(item) for item in data)
    else:
        keys = data

    n = len(data)
    graph = defaultdict(list)

    # Computing similarities
    if processes == 1:
        for i in range(n):
            A = keys[i]

            for j in range(i + 1, n):
                B = keys[j]

                if similarity(A, B):
                    graph[i].append(j)
                    graph[j].append(i)
    else:

        pickled_similarity = dill.dumps(similarity)

        # Iterator
        pool_iter = (
            (pickled_similarity, ) + chunk
            for chunk
            in upper_triangular_matrix_chunk_iter(keys, chunk_size)
        )

        # Pool
        with Pool(processes=processes) as pool:
            for matches in pool.imap(pairwise_worker, pool_iter):
                for i, j in matches:
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

        cluster = [data[i]] + [data[j] for j in neighbors]
        yield cluster


def pairwise_connected_components(data, similarity=None, distance=None, radius=None,
                                  min_size=2, max_size=float('inf'), key=None,
                                  processes=1, chunk_size=100):
    """
    Function returning an iterator over found clusters by computing a
    similarity graph of given data and extracting its connected components.

    It works by assuming the similarity relation is transitive, meaning that
    (A =~ B, B =~ C) leads to A =~ C, which is often quite correct.

    This means two things:
        1) The produced clusters may have a larger radius that what's
           intended.
        2) One item cannot belong to more than one cluster.

    This algorithm runs in O(n * (c - 1) / 2), n being the number of items and
    c being the number of connected components, i.e. O(n^2) in practice since
    for record linkage most items will be alone in their clusters.

    Example:
        The following chain:
            ('abc', 'bcd', 'cde', 'def', 'efg', 'ghi')
        will produce the following levenshtein radius=2 cluster:
            ('abc', 'bcd', 'cde', 'def', 'efg', 'ghi')

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
        key (callable, optional): function returning an item's key.
            Defaults to None.
        processes (number, optional): number of processes to use. Defaults to 1.
        chunk_size (number, optional): size of matrix chunks to send to
            subprocesses. Defaults to 100.

    Yields:
        list: A viable cluster.

    """

    # Formatting similarity
    similarity = make_similarity_function(similarity=similarity, distance=distance, radius=radius)

    # We need to consume as a list to be able of random access
    if type(data) is not list:
        data = list(data)

    if key is not None:
        keys = list(key(item) for item in data)
    else:
        keys = data

    n = len(data)
    sets = UnionFind(n)

    # Computing pairwise distances
    if processes == 1:
        for i in range(n):
            A = keys[i]

            # NOTE: if one adds a cardinality test hear, we get the leader algo

            for j in range(i + 1, n):
                B = keys[j]

                if sets.connected(i, j):
                    continue

                if similarity(A, B):
                    sets.union(i, j)
    else:
        pickled_similarity = dill.dumps(similarity)

        # Iterator
        pool_iter = (
            (pickled_similarity, ) + chunk
            for chunk
            in upper_triangular_matrix_chunk_iter(keys, chunk_size)
        )

        # Pool
        with Pool(processes=processes) as pool:
            for matches in pool.imap_unordered(pairwise_worker, pool_iter):
                for i, j in matches:
                    sets.union(i, j)

    # TODO: Should really be using the sparse version
    for component in sets.components(min_size=min_size, max_size=max_size):
        yield [data[i] for i in component]


def pairwise(data, mode='connected_components', **kwargs):
    """
    Function returning an iterator over found clusters by computing pairwise
    similarity or distance.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        mode (str): 'leader' or 'fuzzy_clusters' or 'connected_components'.
            Defaults to 'connected_components'.
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
    if mode not in ['leader', 'fuzzy_clusters', 'connected_components']:
        raise TypeError('fog.clustering.pairwise: wrong mode "%s"' % mode)

    if mode == 'leader':
        return pairwise_leader(data, **kwargs)

    if mode == 'fuzzy_clusters':
        return pairwise_fuzzy_clusters(data, **kwargs)

    return pairwise_connected_components(data, **kwargs)
