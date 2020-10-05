# =============================================================================
# Fog Dice Coefficient
# =============================================================================
#
# Functions computing the Sørensen-Dice coefficient.
#
# [Urls]:
# https://en.wikipedia.org/wiki/S%C3%B8rensen%E2%80%93Dice_coefficient
#
# [References]:
# Dice, Lee R. (1945). "Measures of the Amount of Ecologic Association
# Between Species". Ecology 26 (3): 297–302.
#
from fog.metrics.utils import ACCEPTABLE_TYPES


def dice_coefficient(A, B):
    """
    Function computing the Dice coefficient. That is to say twice the size of
    the intersection of both sets divided by the sum of both their sizes.

    Runs in O(n), n being the size of the smallest set.

    Args:
        A (iterable): First sequence.
        B (iterable): Second sequence.

    Returns:
        float: Dice coefficient between A & B.

    Example:
        from fog.metrics import dice_coefficient

        # Basic
        dice_coefficient('context', 'contact')
        >>> ~0.727

    """
    if A is B:
        return 1.0

    if not isinstance(A, ACCEPTABLE_TYPES):
        A = set(A)

    if not isinstance(B, ACCEPTABLE_TYPES):
        B = set(B)

    # Swapping to iterate over smaller set and minimize lookups
    if len(A) > len(B):
        A, B = B, A

    la = len(A)
    lb = len(B)

    if la == 0:
        return 1.0 if lb == 0 else 0.0

    # Counting intersection
    I = 0

    for v in A:
        if v in B:
            I += 1

    return (2 * I) / (la + lb)
