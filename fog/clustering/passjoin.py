# =============================================================================
# Fog PassJoin Clustering
# =============================================================================
#
# Implementation of the PassJoin algorithm.
#
# [References]:
# Jiang, Yu, Dong Deng, Jiannan Wang, Guoliang Li, et Jianhua Feng.
# « Efficient Parallel Partition-Based Algorithms for Similarity Search and Join
# with Edit Distance Constraints ». In Proceedings of the Joint EDBT/ICDT 2013
# Workshops on - EDBT ’13, 341. Genoa, Italy: ACM Press, 2013.
# https://doi.org/10.1145/2457317.2457382.
#
# Li, Guoliang, Dong Deng, et Jianhua Feng. « A Partition-Based Method for
# String Similarity Joins with Edit-Distance Constraints ». ACM Transactions on
# Database Systems 38, no 2 (1 juin 2013): 1‑33.
# https://doi.org/10.1145/2487259.2487261.
#
# [Urls]:
# http://people.csail.mit.edu/dongdeng/projects/passjoin/index.html
#
from collections import defaultdict
from fog.clustering.utils import clusters_from_pairs


def count_substrings_l(k, s, l):
    """
    Function returning the number of substrings that will be selected by the
    multi-match-aware selection scheme for theshold `k`, for a string of length
    `s` to match strings of length `l`.

    Args:
        k (int): Levenshtein distance threshold.
        s (int): Length of target strings.
        l (int): Length of strings to match.

    Returns:
        int: The number of selected substrings.

    """
    return ((k ** 2 - abs(s - l) ** 2) // 2) + k + 1


def count_keys(k, s):
    """
    Function returning the minimum number of substrings that will be selected by
    the multi-match-aware selection scheme for theshold `k`, for a string of
    length `s` to match any string of relevant length.

    Note that for queries, this number will be higher => range(s - k, s + k + 1).

    Args:
        k (int): Levenshtein distance threshold.
        s (int): Length of target strings.

    Returns:
        int: The number of selected substrings.

    """

    c = 0

    for l in range(s - k, s + 1):
        c += count_substrings_l(k, s, l)

    return c


def sort_key(string):
    """
    Function returning sort value for the strings in PassJoin algorithm. It
    basically order them by decreasing length, then alphabetically as per
    the "4.2 Effective Indexing Strategy" point of the paper.
    """
    return -len(string), string


def partition(k, l):
    """
    Function partitioning a string into k + 1 uneven segments, the shorter
    ones, then the longer ones.

    Args:
        k (int): Levenshtein distance threshold.
        l (int): Length of the string.

    Yields:
        tuple: index, start, length.

    """
    m = k + 1
    a = l // m
    b = a + 1

    large_segments = l - a * m
    small_segments = m - large_segments

    for i in range(small_segments):
        yield (i, i * a, a)

    offset = i * a + a

    for j in range(large_segments):
        yield (i + 1 + j, offset + j * b, b)


def segments(k, string):
    """
    Function yielding a string's k + 1 passjoin segments to index.

    Args:
        k (int): Levenshtein distance threshold.
        string (str): Target string.

    Yields:
        tuple: index, segment.

    """
    for i, start, length in partition(k, len(string)):
        yield (i, string[start:start + length])


def multi_match_aware_interval(k, delta, i, s, pi, li):
    """
    Function returning the interval of relevant substrings to lookup using the
    multi-match-aware substring selection scheme described in the paper.

    Args:
        k (int): Levenshtein distance threshold.
        delta (int): Signed length difference between both considered strings.
        i (int): k + 1 segment index.
        s (int): string length.
        pi (int): k + 1 segment position in target string.
        li (int): k + 1 segment length.

    Returns:
        tuple: start, stop of the interval.

    """
    start1 = pi - i
    end1 = pi + i

    o = k - i

    start2 = pi + delta - o
    end2 = pi + delta + o

    end3 = s - li

    return max(0, start1, start2), min(end1, end2, end3)


def multi_match_aware_substrings(k, string, l, i, pi, li):
    """
    Function yielding relevant substrings to lookup using the multi-match-aware
    substring selection scheme described in the paper.

    Args:
        k (int): Levenshtein distance threshold.
        string (str): Target string.
        l (int): Length of strings to match.
        i (int): k + 1 segment index.
        pi (int): k + 1 segment position in target string.
        li (int): size in characters of the k + 1 segment.

    Yields:
        str: one of the contiguous substrings.

    """
    s = len(string)

    # Note that we need to keep the non-absolute delta for this function
    # to work in both directions, up & down
    delta = s - l

    start, stop = multi_match_aware_interval(k, delta, i, s, pi, li)

    current_substring = None

    for j in range(start, stop + 1):
        substring = string[j:j + li]

        # We skip identical consecutive substrings (to avoid repetition in
        # case of contiguous letter duplication)
        if substring == current_substring:
            continue

        yield substring

        current_substring = substring


def passjoin(data, k, distance, sort=True, min_size=2, max_size=float('inf'),
             mode='connected_components'):
    """
    Function returning an iterator over found clusters using the PassJoin
    algorithm that is able to find every pair of strings having a Levenshtein
    distance less than or equal to a threshold k.

    It works by indexing k + 1 mostly even segments of the considered strings
    into inverted indices splitted by string length and segment index. Then,
    we use another complex but comprehensive string partition scheme to be able
    to produce candidate pairs which are verified using Levenshtein distance.

    It runs in approximately O(nk^2) or O(nk^3) if not sorted. It's therefore
    very scalable with small k values and is undoubtedly better than the naive
    quadratic approach.

    Args:
        data (iterable): Arbitrary iterable containing data points to gather
            into clusters. Will be fully consumed.
        k (number): Levenshtein distance threshold.
        distance (callable): Function tasked to compute the Levenshtein distance
            between two points of data.
        sort (boolean, optional): whether to sort the data beforehand. Defaults
            to True.
        min_size (number, optional): minimum number of items in a cluster for
            it to be considered viable. Defaults to 2.
        max_size (number, optional): maximum number of items in a cluster for
            it to be considered viable. Defaults to infinity.
        mode (string, optional): 'fuzzy_clusters', 'connected_components'.
            Defaults to 'connected_components'.

    Yields:
        list: A viable cluster.

    """

    if sort:

        # NOTE: sorting in reverse as per "4.2 Effective Indexing Strategy"
        data = sorted(data, key=sort_key)

    # TODO: when keys lengths are <= k some pairs are tested more than once!
    # TODO: test exact match cases
    # TODO: empty string should probably be handled in its own way?

    def clustering():
        L = defaultdict(lambda: defaultdict(list))
        Ll = None

        for A in data:
            s = len(A)

            # Attempting to match the string
            for l in range(s if sort else max(0, s - k), s + k + 1):
                Ll = L.get(l)

                # Index is empty for this length, no need to enquire further
                if Ll is None:
                    continue

                for i, start, length in partition(k, l):
                    for substring in multi_match_aware_substrings(k, A, l, i, start, length):
                        candidates = Ll.get((i, substring))

                        if candidates is None:
                            continue

                        for B in candidates:

                            # NOTE: first condition is here not to compute Levenshtein
                            # distance for tiny strings
                            # NOTE: a pair may arise more than once here
                            # It's taken care of later but I feel we can do better...
                            # What's more, we should also record non-matches even if the
                            # case of testing twice is naturally rarer
                            if (s <= k and l <= k) or distance(A, B) <= k:
                                yield (A, B)

            # Indexing the string
            # NOTE: it's possible to cleanup some memory when working on sorted strings
            Ll = L[s]

            for key in segments(k, A):
                Ll[key].append(A)

    yield from clusters_from_pairs(
        clustering(),
        min_size=min_size,
        max_size=max_size,
        mode=mode
    )
