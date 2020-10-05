# =============================================================================
# Fog Metrics Utilities
# =============================================================================
#
# Miscellaneous utility functions used to compute metrics
#
ACCEPTABLE_TYPES = (set, frozenset, dict)


def intersection_size(A, B):
    if A is B:
        return len(A)

    if not isinstance(A, ACCEPTABLE_TYPES):
        A = set(A)

    if not isinstance(B, ACCEPTABLE_TYPES):
        B = set(B)

    if len(A) > len(B):
        A, B = B, A

    if len(A) == 0:
        return 0

    i = 0

    for x in A:
        if x in B:
            i += 1

    return i
