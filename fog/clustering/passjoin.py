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
        c += count_keys_l(k, s, l)

    return c


def multi_match_aware_interval(k, delta, i, pi):
    """
    Function returning the interval of relevant substrings to lookup using the
    multi-match-aware substring selection scheme described in the paper.

    Args:
        k (int): Levenshtein distance threshold.
        delta (int): Signed length difference between both considered strings.
        i (int): k + 1 segment index.
        pi (int): k + 1 segment position in target string.

    Returns:
        tuple: start, stop of the interval.

    """
    start1 = pi - i
    end1 = pi + i

    o = k - i

    start2 = pi + delta - o
    end2 = pi + delta + o

    return max(start1, start2), min(end1, end2)


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
