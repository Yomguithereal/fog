# =============================================================================
# Fog Jaccard Similarity
# =============================================================================
#
# Functions computing the Jaccard similarity
#
# [Urls]:
# https://en.wikipedia.org/wiki/Jaccard_index
# https://pdfs.semanticscholar.org/74be/e1ebf204dba4b2da0399a25a5ac9253a824e.pdf
#
# [References]:
# Jaccard, Paul (1912), “The distribution of the flora in the alpine zone”,
# New Phytologist 11: 37–50
#
# Ioffe, "Improved Consistent Sampling, Weighted Minhash and L1 Sketching".
#
from fog.metrics.utils import ACCEPTABLE_TYPES


def jaccard_similarity(A, B):
    """
    Function computing the Jaccard similarity. That is to say the intersection
    of input sets divided by their union.

    Runs in O(n), n being the size of the smallest set.

    Args:
        A (iterable): First sequence.
        B (iterable): Second sequence.

    Returns:
        float: Jaccard similarity between A & B.

    Example:
        from fog.metrics import jaccard_similarity

        # Basic
        jaccard_similarity('context', 'contact')
        >>> ~0.571

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

    # Size of the union is size of A + size of B - intersection
    U = len(A) + len(B) - I

    return I / U


def weighted_jaccard_similarity(A, B):
    """
    Function computing the weighted Jaccard similarity.

    Runs in O(n), n being the sum of A & B's sizes.

    Args:
        A (Counter): First weighted set.
        B (Counter): Second weighted set.

    Returns:
        float: Weighted Jaccard similarity between A & B.

    Example:
        from fog.metrics import weighted_jaccard_similarity

        # Basic
        weighted_jaccard_similarity({'apple': 34, 'pear': 3}, {'pear': 1, 'orange': 1})
        >>> ~0.026

    """

    # Early termination
    if A is B:
        return 1.0

    if len(A) == 0 or len(B) == 0:
        return 0.0

    I = 0.0
    U = 0.0

    done = set()

    # Swapping to iterate over smaller set and minimize lookups
    if len(A) > len(B):
        A, B = B, A

    # Computing intersection
    for k, weight_A in A.items():
        weight_B = B.get(k, 0.0)

        if weight_B != 0.0:
            done.add(k)

        if weight_A < weight_B:
            I += weight_A
            U += weight_B
        else:
            I += weight_B
            U += weight_A

    # Finalizing union
    for k, v in B.items():
        if k in done:
            continue

        U += v

    return I / U
