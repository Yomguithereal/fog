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

FLAG = '\x00'


def levenshtein_1d(string, transpositions=False):
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
