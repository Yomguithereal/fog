# =============================================================================
# Fog Cosine Similarity
# =============================================================================
#
# Functions computing the cosine similarity.
#
# [Url]:
# https://en.wikipedia.org/wiki/Cosine_similarity
#
from collections import Counter
import math


def sparse_cosine_similarity(A, B):
    """
    Function computing cosine similarity on sparse weighted sets represented
    by python dicts.

    Runs in O(n), n being the sum of A & B's sizes.

    Args:
        A (Counter): First weighted set.
        B (Counter): Second weighted set.

    Returns:
        float: Cosine similarity between A & B.

    """

    # Early termination
    if A is B:
        return 1.0

    if len(A) == 0 or len(B) == 0:
        return 0.0

    xx = 0.0
    xy = 0.0
    yy = 0.0

    # Swapping to iterate over smaller set and minimize lookups
    if len(A) > len(B):
        A, B = B, A

    for k, v in A.items():
        weight = v
        xx += weight ** 2

        v2 = B.get(k)

        if v2 is not None:
            xy += weight * v2

    for v in B.values():
        weight = v
        yy += weight ** 2

    return xy / math.sqrt(xx * yy)


def sparse_dot_product(A, B):
    """
    Function used to compute the dotproduct of sparse weighted sets represented
    by python dicts.

    Runs in O(n), n being the size of the smallest set.

    Args:
        A (Counter): First weighted set.
        B (Counter): Second weighted set.

    Returns:
        float: Dot product of A & B.

    """

    # Swapping so we iterate over the smallest set
    if len(A) > len(B):
        A, B = B, A

    product = 0.0

    for k, w1 in A.items():
        w2 = B.get(k)

        if w2 is not None:
            product += w1 * w2

    return product


def cosine_similarity(A, B):
    """
    Function computing the cosine similarity of the given sequences.

    Runs in O(n), n being the sum of A & B's sizes.

    Args:
        A (iterable): First sequence.
        B (iterable): Second sequence.

    Returns:
        float: Cosine similarity between A & B.

    """

    # Computing frequencies
    A = Counter(A)
    B = Counter(B)

    return sparse_cosine_similarity(A, B)
