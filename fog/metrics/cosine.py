# =============================================================================
# Fog Cosine Similarity
# =============================================================================
#
# Functions computing the cosine similarity.
#
import math


def sparse_cosine_similarity(A, B):
    '''
    Function computing cosine similarity on sparse weighted sets represented
    by python Counter instances.

    Args:
        A (Counter): First weighted set.
        B (Counter): Second weighted set.

    Returns:
        float: Cosine similarity between A & B.
    '''
    xx = 0
    xy = 0
    yy = 0

    # Swapping to iterate over smaller set and minimize lookups
    if len(A) > len(B):
        A, B = B, A

    for key, weight in A.items():
        xx += weight ** 2

        if key in B:
            xy += weight * B[key]

    for weight in B.values():
        yy += weight ** 2

    return xy / math.sqrt(xx * yy)
