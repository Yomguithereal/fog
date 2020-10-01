# =============================================================================
# Fog Metrics Utilities
# =============================================================================
#
# Miscellaneous utility functions used to compute metrics
#


def intersection_size(A, B):
    if A is B:
        return len(A)

    if len(A) > len(B):
        A, B = B, A

    if len(A) == 0:
        return 0

    i = 0

    for x in A:
        if x in B:
            i += 1

    return i
