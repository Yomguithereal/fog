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


def multi_match_aware_interval(k, delta, i, pi):
    """
    Function returning the interval of relevant substrings to lookup using the
    multimatch-aware substring selection scheme described in the paper.

    Args:
        k (int): Distance threshold.
        delta (int): Signed length difference between both considered strings.
        i (int): k+1 segment index.
        pi (int): k+1 segment position in target string.

    Returns:
        tuple: start, stop of the interval.

    """
    start1 = pi - i
    end1 = pi + i

    o = k - i

    start2 = pi + delta - o
    end2 = pi + delta + o

    return max(start1, start2), min(end1, end2)
