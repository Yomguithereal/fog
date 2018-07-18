# =============================================================================
# Fog Levenshtein Distance
# =============================================================================
#
# Functions related to the Levenshtein or "edit" distance.
#
# [Urls]:
# https://en.wikipedia.org/wiki/Levenshtein_distance
# https://github.com/gustf/js-levenshtein
# https://github.com/Yomguithereal/talisman
#
# [Reference]:
# Levenshtein, Vladimir I. (February 1966). "Binary codes capable of
# correcting deletions, insertions, and reversals".
# Soviet Physics Doklady 10 (8): 707–710.
#
# Optimized pure python implementation with:
#   - Single vector.
#   - Loop unrolling optimizations (Gustaf Andersson).
#   - Prefix-Suffix trimming (Guillaume Plique).
#
import cython
from libc.stdlib cimport malloc, free


cdef unsigned int min_cost(
    unsigned int d0,
    unsigned int d1,
    unsigned int d2,
    unsigned char bx,
    unsigned char ay
):
    if d0 < d1 or d2 < d1:
        if d0 > d2:
            return d2 + 1
        else:
            return d0 + 1
    else:
        if bx == ay:
            return d1
        else:
            return d1 + 1


@cython.boundscheck(False)
def levenshtein_distance(str A, str B):
    if A is B or A == B:
        return 0

    cdef unsigned int LA = len(A)
    cdef unsigned int LB = len(B)

    if LA > LB:
        A, B = B, A
        LA, LB = LB, LA

    while LA > 0 and A[LA - 1] == B[LB - 1]:
        LA -= 1
        LB -= 1

    cdef unsigned int offset = 0

    while offset < LA and A[offset] == B[offset]:
        offset += 1

    LA -= offset
    LB -= offset

    if LA == 0 or LB < 3:
        return LB

    cdef unsigned int V = 2 * LA
    cdef unsigned int *vector = <unsigned int *> malloc(V * sizeof(unsigned int))

    cdef unsigned int x = 0
    cdef unsigned int y = 0
    cdef unsigned int t = 0

    while y < LA:
        t = y * 2
        vector[t] = y + 1
        vector[t + 1] = ord(A[offset + y])
        y += 1

    cdef unsigned int d0
    cdef unsigned int d1
    cdef unsigned int d2
    cdef unsigned int d3

    cdef unsigned char ay

    cdef unsigned int dd
    cdef unsigned int dy

    cdef unsigned char bx0
    cdef unsigned char bx1
    cdef unsigned char bx2
    cdef unsigned char bx3

    while x + 3 < LB:
        d0 = x
        d1 = x + 1
        d2 = x + 2
        d3 = x + 3

        bx0 = ord(B[offset + d0])
        bx1 = ord(B[offset + d1])
        bx2 = ord(B[offset + d2])
        bx3 = ord(B[offset + d3])

        x += 4
        dd = x

        y = 0

        while y < V:
            dy = vector[y]
            ay = vector[y + 1]
            d0 = min_cost(dy, d0, d1, bx0, ay)
            d1 = min_cost(d0, d1, d2, bx1, ay)
            d2 = min_cost(d1, d2, d3, bx2, ay)
            dd = min_cost(d2, d3, dd, bx3, ay)
            vector[y] = dd
            d3 = d2
            d2 = d1
            d1 = d0
            d0 = dy

            y += 2

    while x < LB:
        d0 = x
        bx0 = ord(B[offset + d0])
        x += 1
        dd = x

        y = 0

        while y < V:
            dy = vector[y]

            if dy < d0 or dd < d0:
                if dy > dd:
                    dd = dd + 1
                else:
                    dd = dy + 1
            else:
                if bx0 == vector[y + 1]:
                    dd = d0
                else:
                    dd = d0 + 1

            vector[y] = dd
            d0 = dy

            y += 2

    free(vector)

    return dd
