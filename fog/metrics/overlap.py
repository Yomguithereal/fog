# =============================================================================
# Fog Overlap Coefficient
# =============================================================================
#
# Functions computing the overlap coefficient.
#
# [Urls]:
# https://en.wikipedia.org/wiki/Overlap_coefficient
#
from fog.metrics.utils import ACCEPTABLE_TYPES


def overlap_coefficient(A, B):
    """
    Function computing the overlap coefficient of the given sets, i.e. the size
    of their intersection divided by the size of the smallest set.

    Runs in O(n), n being the size of the smallest set.

    Args:
        A (iterable): First sequence.
        B (iterable): Second sequence.

    Returns:
        float: overlap coefficient between A & B.

    """
    if A is B:
        return 1.0

    if not isinstance(A, ACCEPTABLE_TYPES):
        A = set(A)

    if not isinstance(B, ACCEPTABLE_TYPES):
        B = set(B)

    if len(A) == 0 or len(B) == 0:
        return 0.0

    # Swapping to iterate over smaller set and minimize lookups
    if len(A) > len(B):
        A, B = B, A

    # Counting intersection
    I = 0

    for v in A:
        if v in B:
            I += 1

    return I / min(len(A), len(B))
