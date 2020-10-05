# =============================================================================
# Fog Sorted Neighborhood Clustering
# =============================================================================
#
# Implementation of the Sorted Neighborhood method.
#
# [References]:
# Mauricio A. Hernandez and Salvatore J. Stolfo. The merge/purge problem for
# large databases. In Proceedings of the ACM International Conference on
# Management of Data (SIGMOD), 1995.
#
# Mauricio A. Hernandez and Salvatore J. Stolfo. Real-world data is dirty:
# Data cleansing and the merge/purge problem. Data Mining and Knowledge
# Discovery, 2(1), 1998
#
# Yan, Su, Dongwon Lee, Min-Yen Kan, et Lee C. Giles. « Adaptive Sorted
# Neighborhood Methods for Efficient Record Linkage », 185. ACM Press, 2007.
# https://doi.org/10.1145/1255175.1255213.
#
# [Urls]:
# https://hpi.de/fileadmin/user_upload/fachgebiete/naumann/folien/SS13/DPDC/DPDC_14_SNM.pdf
#
from fog.clustering.utils import make_similarity_function, clusters_from_pairs

# TODO: parallelize
# TODO: default zigzag
# TODO: multipass snm variant


def sorted_neighborhood(data, key=None, keys=None, similarity=None, distance=None,
                        radius=None, window=10, min_size=2, max_size=float('inf'),
                        mode='connected_components'):
    """
    Function returning an iterator over found clusters using the sorted
    neighborhood method (SNM).

    It works by first sorting the data according to a key which could, if
    cleverly chosen, put similar items next to one another in the result.

    We then attempt to find clusters by computing pairwise similarity/distances
    in small blocks of constant size in the sorted list.

    Omission key & skeleton keys by Pollock & Zamora are a good choice of
    sorting key if you try to find mispellings, for instance.

    Other good choice of keys is a combination of sorting strings
    lexicographically and sorting them reversed ([None, lambda x: x[::-1]]).

    Note that the sorted neighboorhood method usually runs faster than blocking
    but also misses much more true positives.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        key (callable, optional): key on which to sort the data.
        keys (iterable, optional): list of keys on which to sort for multipass
            sorted neighborhood method.
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
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.

    Yields:
        list: A viable cluster.

    """

    # Formatting similarity
    similarity = make_similarity_function(similarity=similarity, distance=distance, radius=radius)

    # Iterating over sorted data
    def clustering():
        multipass_keys = keys if keys is not None else [key]

        for k in multipass_keys:
            S = sorted(data, key=k)
            n = len(S)

            for i in range(n):
                A = S[i]

                for j in range(i + 1, min(n, i + window)):
                    B = S[j]

                    if similarity(A, B):
                        yield (A, B)

    # Building clusters
    yield from clusters_from_pairs(
        clustering(),
        min_size=min_size,
        max_size=max_size,
        mode=mode,
        fuzzy=keys is not None
    )


def full_AA_SNM(sorted_records, similarity, window):
    n = len(sorted_records)
    w = window
    step = w - 1
    first = 0
    last = first + step

    while last < n:
        f = first

        # Enlargement
        while similarity(sorted_records[first], sorted_records[last]):
            w = last - f + 1
            first = last
            last = first + w - 1

        # Retrenchment
        w = last - f + 1

        while w > window:
            previous = last - 1

            if similarity(sorted_records[previous], sorted_records[last]):
                break

            # NOTE: possibility to divide the window by two according to
            # the paper.
            w -= 1
            last = previous

        w = window

        yield (f, last)

        first = last + 1
        last = first + step

    if first < n:
        yield (first, n - 1)


def adaptive_sorted_neighborhood(data, key=None, keys=None, similarity=None,
                                 distance=None, radius=None, window=10,
                                 min_size=2, max_size=float('inf'),
                                 mode='connected_components'):
    """
    Function returning an iterator over found clusters using the adaptive
    sorted neighborhood method (ASNM).

    More specifically, this method implements the "Full-Accumulatively-Adaptative
    SNM" from the "Adaptive Sorted Neighborhood Methods for Efficient
    Record Linkage" paper.

    Note that this method is more precise that basic SNM only for cases where
    duplicate components are sufficiently large and when the variance
    of their size is important. Else it's basically useless.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        key (callable, optional): key on which to sort the data.
        keys (iterable, optional): list of keys on which to sort for multipass
            sorted neighborhood method.
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
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.

    Yields:
        list: A viable cluster.

    """

    # Formatting similarity
    similarity = make_similarity_function(similarity=similarity, distance=distance, radius=radius)

    # Iterating over sorted data
    def clustering():
        multipass_keys = keys if keys is not None else [key]

        for k in multipass_keys:
            S = sorted(data, key=k)

            for start, end in full_AA_SNM(S, similarity, window):
                l = end - start + 1

                if l == 1:
                    continue

                elif l == 2:
                    A = S[start]
                    B = S[end]

                    if similarity(A, B):
                        yield (A, B)

                else:
                    for i in range(start, end + 1):
                        for j in range(i + 1, end + 1):
                            A = S[i]
                            B = S[j]

                            if similarity(A, B):
                                yield (A, B)

    # Building clusters
    yield from clusters_from_pairs(
        clustering(),
        min_size=min_size,
        max_size=max_size,
        mode=mode,
        fuzzy=keys is not None
    )
