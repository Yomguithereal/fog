# =============================================================================
# Fog Jaccard Similarity
# =============================================================================
#
# Functions computing the Jaccard similarity
#


def weighted_jaccard_similarity(A, B):
    """
    Function computing the weighted Jaccard similarity.

    [Reference]:
    Ioffe, "Improved Consistent Sampling, Weighted Minhash and L1 Sketching".

    [Url]:
    https://pdfs.semanticscholar.org/74be/e1ebf204dba4b2da0399a25a5ac9253a824e.pdf

    Runs in O(n), n being the sum of A & B's sizes.

    Args:
        A (Counter): First weighted set.
        B (Counter): Second weighted set.

    Returns:
        float: Weighted Jaccard similarity between A & B.

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
    for k, v in A.items():
        weight_A = v
        weight_B = 0.0

        v2 = B.get(k)

        if v2 is not None:
            weight_B = v2
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
