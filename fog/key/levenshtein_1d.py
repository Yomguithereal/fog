# =============================================================================
# Fog Levensthein 1D Key
# =============================================================================
#
# Key function returning a series of keys that one can index in a dict to
# make strings having a Levenshtein distance of 1 collide.
#
# Under the hood it works by producing every substitution key then every
# addition key (deletion keys are redundant with addition keys and will
# produce wrong collisions such as "abc" & "adb").
#
# Note that it's also possible to generate transpostion keys.
#
from functools import partial

FLAG = '\x00'


def levenshtein_1d_keys(string, transpositions=False):
    """
    Function returning an iterator over Levenshtein 1D keys, being the series
    of keys colliding with other strings being at a Levenshtein distance of
    1 with the given string.

    Those keys are useful to perform O(n) clustering with Levenshtein
    distance <= 1 but can become very costly with long strings since the number
    of produced keys is a factor of your string's length.

    Args:
        string (string): Target string
        transpositions (bool, optional): Whether to support transpositions
            like with the Damerau-Levenshtein distance. Defaults to False.

    Yields:
        string: A single Levenshtein 1D key.

    """

    n = len(string)

    yield string

    for i in range(n):

        # Substitution
        yield string[:i] + FLAG + string[i + 1:]

        # Transpositions
        if i > 0 and transpositions:
            if string[i - 1] == string[i]:
                continue

            yield string[:i - 1] + string[i] + string[i - 1] + string[i + 1:]

        # Additions
        if i > 0 and string[i - 1] == string[i]:
            continue

        yield string[:i] + FLAG + string[i:]

    # Last addition
    yield string + FLAG


damerau_levenshtein_1d_keys = partial(levenshtein_1d_keys, transpositions=True)


# TODO: transpositions, TODO: marking start and end
def levenshtein_1d_blocks(string):
    """
    Function returning the minimal set of longest Levenshtein distance <= 1
    blocking keys of target string. Under the hood, this splits the given
    string into an average of 3 blocks (2 when string length is even, 4 when
    odd).

    Args:
        string (str): Target string.

    Returns:
        tuple: Resulting blocks.

    """
    n = len(string)

    if n == 1:
        return (string, )

    h = n // 2

    # String has even length, we just split in half
    if n % 2 == 0:
        first_half = string[:h]
        second_half = string[h:]

        if first_half == second_half:
            return (first_half, )

        return (first_half, second_half)

    # String has odd length, we split twice
    h1 = h + 1

    first_half = string[:h]
    second_half = string[h:]
    first_half1 = string[:h1]
    second_half1 = string[h1:]

    if first_half == second_half1:
        return (first_half, second_half1, first_half1)

    if second_half == first_half1:
        return (first_half, second_half, second_half1)

    return (first_half, second_half, first_half1, second_half1)