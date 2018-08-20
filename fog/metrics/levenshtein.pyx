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
# Note that this is still slower than python-Levensthein.
#
import cython
from libc.stdlib cimport malloc, free


@cython.boundscheck(False)
def levenshtein_distance(str A, str B):
    """
    Function computing the Levenshtein distance between two given strings.

    Runs in O(mn), m being the size of the first string and n the size of the
    second one.

    Args:
        A (str): First string.
        B (str): Second string.

    Returns:
        float: Levenshtein distance between A & B.

    """

    if A is B or A == B:
        return 0

    cdef unsigned int LA = len(A)
    cdef unsigned int LB = len(B)

    if LA > LB:
        A, B = B, A
        LA, LB = LB, LA

    # Ignoring common suffix
    while LA > 0 and A[LA - 1] == B[LB - 1]:
        LA -= 1
        LB -= 1

    # Ignoring common prefix
    cdef unsigned int start = 0

    while start < LA and A[start] == B[start]:
        start += 1

    LA -= start
    LB -= start

    if LA == 0:
        return LB

    if LA == 1:
        if A[start] in B:
            return LB - 1

        return LB

    cdef unsigned short *codes = <unsigned short *> malloc(LB * sizeof(unsigned short))
    cdef unsigned int *vector = <unsigned int *> malloc(LB * sizeof(unsigned int))

    cdef unsigned int i = 0

    while i < LB:
        codes[i] = ord(B[start + i])
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
        charA = ord(A[start + i])

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

    return current


@cython.boundscheck(False)
def limited_levenshtein_distance(unsigned int max_distance, str A, str B):
    """
    Function computing the limited Levenshtein distance between two given
    strings, i.e. if the distance between A & B is over the given maximum, the
    function will stop computing and return an upper bound of max_distance + 1.

    This is really usefull when you want to find similar strings and want
    to optimize for speed. This is really usefull when the considered strings
    are long.

    Args:
        max_distance (number): Maximum allowable distance between A & B.
        A (str): First string.
        B (str): Second string.

    Returns:
        float: Levenshtein distance between A & B or an upper bound.

    """

    if A is B or A == B:
        return 0

    cdef unsigned int upper_bound = max_distance + 1

    cdef unsigned int LA = len(A)
    cdef unsigned int LB = len(B)

    if LA > LB:
        A, B = B, A
        LA, LB = LB, LA

    if LA == 0:
        return upper_bound if LB > max_distance else LB

    # Ignoring common suffix
    while LA > 0 and A[LA - 1] == B[LB - 1]:
        LA -= 1
        LB -= 1

    if LA == 0:
        return upper_bound if LB > max_distance else LB

    # Ignoring common prefix
    cdef unsigned int start = 0

    while start < LA and A[start] == B[start]:
        start += 1

    LA -= start
    LB -= start

    if LA == 0:
        return upper_bound if LB > max_distance else LB

    cdef unsigned int diff = LB - LA

    if max_distance > LB:
        max_distance = LB
    elif diff > max_distance:
        return upper_bound

    cdef unsigned short *codes = <unsigned short *> malloc(LB * sizeof(unsigned short))
    cdef unsigned int *vector = <unsigned int *> malloc(LB * sizeof(unsigned int))

    cdef unsigned int i = 0

    while i < max_distance:
        codes[i] = ord(B[start + i])
        vector[i] = i + 1
        i += 1

    while i < LB:
        codes[i] = ord(B[start + i])
        vector[i] = upper_bound
        i += 1

    cdef unsigned int offset = max_distance - diff
    cdef bint have_max = max_distance < LB

    cdef unsigned int j_start = 0
    cdef unsigned int j_end = max_distance

    cdef unsigned int current = 0
    cdef unsigned int left
    cdef unsigned int above
    cdef unsigned int charA
    cdef unsigned int j

    i = 0

    while i < LA:
        left = i
        current = i + 1

        charA = ord(A[start + i])
        j_start += 1 if i > offset else 0
        j_end += 1 if j_end < LB else 0

        j = j_start

        while j < j_end:
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

        if have_max and vector[i + diff] > max_distance:
            return upper_bound

        i += 1

    free(codes)
    free(vector)

    return current if current <= max_distance else upper_bound
