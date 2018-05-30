# =============================================================================
# Fog Cosine Similarity
# =============================================================================
#
# Functions computing the cosine similarity.
#
import math


def sparse_cosine_similarity(A, B, key=lambda x: x):
    """
    Function computing cosine similarity on sparse weighted sets represented
    by python dicts.

    Runs in O(n), n being the sum of A & B's sizes.

    Args:
        A (Counter): First weighted set.
        B (Counter): Second weighted set.
        key (callable, optional): Function retrieving the weight from item.

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
        weight = key(v)
        xx += weight ** 2

        v2 = B.get(k)

        if v2 is not None:
            xy += weight * key(v2)

    for v in B.values():
        weight = key(v)
        yy += weight ** 2

    return xy / math.sqrt(xx * yy)
