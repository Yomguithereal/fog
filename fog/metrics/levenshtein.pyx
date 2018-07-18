# =============================================================================
# Fog Levenshtein Distance
# =============================================================================
#
# Functions related to the Levenshtein or "edit" distance.
#
# [Urls]:
# https://en.wikipedia.org/wiki/Levenshtein_distance
# https://github.com/Yomguithereal/talisman
#
# [Reference]:
# Levenshtein, Vladimir I. (February 1966). "Binary codes capable of
# correcting deletions, insertions, and reversals".
# Soviet Physics Doklady 10 (8): 707–710.
#
import cython
from libc.stdlib cimport malloc, free


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

    if LA == 0:
        return LB

    cdef unsigned short *codes = <unsigned short *> malloc(LB * sizeof(unsigned short))
    cdef unsigned int *vector = <unsigned int *> malloc(LB * sizeof(unsigned int))

    cdef unsigned int i = 0

    while i < LB:
        codes[i] = ord(B[offset + i])
        vector[i] = i + 1
        i += 1

    cdef unsigned int current = 0
    cdef unsigned int left = 0
    cdef unsigned int above = 0
    cdef unsigned short charA = 0
    cdef unsigned int j = 0

    i = 0

    while i < LA:
        left = i
        current = i + 1
        charA = ord(A[offset + i])

        j = 0

        while j < LB:
            above = current

            current = left
            left = vector[j]

            if charA != codes[j]:

                # Insertion
                if left < current:
                    current = left

                # Deletion
                if above < current:
                    current = above

                current += 1

            vector[j] = current

            j += 1


        i += 1

    free(codes)
    free(vector)

    return int(current)
