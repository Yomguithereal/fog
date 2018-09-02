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

# TODO: link to "Indexing Methods for Approximate Dictionary Searching: Comparative Analysis"
from functools import partial


# TODO: note that this is called full-neighborhood generation
# TODO: note that my impl seems to be better because alphabet-agnostic & addition over deletion
def levenshtein_1d_keys(string, transpositions=False, flag='\x00'):
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
        yield string[:i] + flag + string[i + 1:]

        # Transpositions
        if i > 0 and transpositions:
            if string[i - 1] == string[i]:
                continue

            yield string[:i - 1] + string[i] + string[i - 1] + string[i + 1:]

        # Additions
        # Note: I use additions here and not deletions because indexing
        # on deletions can generate false positives such as:
        # "abcd", "abde" -> key "abd".
        # Note: for k = 1, an addition for A->B is compulsorily a deletion
        # for B->A.
        if i > 0 and string[i - 1] == string[i]:
            continue

        yield string[:i] + flag + string[i:]

    # Last addition
    yield string + flag


damerau_levenshtein_1d_keys = partial(levenshtein_1d_keys, transpositions=True)


def levenshtein_1d_blocks(string, transpositions=False, flag='\x00'):
    """
    Function returning the minimal set of longest Levenshtein distance <= 1
    blocking keys of target string. Under the hood, this splits the given
    string into an average of 3 blocks (2 when string length is even, 4 when
    odd). When supporting transpositions, the function will always return
    4 blocks to handle the case when middle letters are transposed.

    Note that this method therefore yields a constant number of keys, as
    opposed to ngrams which yield a number of keys proportional to the size
    of the given strings.

    Args:
        string (str): Target string.
        transpositions (bool, optional): Whether to support transpositions
            like with the Damerau-Levenshtein distance. Defaults to False.

    Returns:
        tuple: Resulting blocks.

    """
    n = len(string)

    if n == 1:
        return (flag + string, string + flag, flag)

    h = n // 2

    # String has even length, we just split in half
    if n % 2 == 0 and not transpositions:
        first_half = flag + string[:h]
        second_half = string[h:] + flag

        return (first_half, second_half)

    # String has odd length, we split twice
    h1 = h + 1

    first_half = flag + string[:h]
    second_half = string[h:] + flag
    first_half1 = flag + string[:h1]
    second_half1 = string[h1:] + flag

    return (first_half, second_half, first_half1, second_half1)


damerau_levenshtein_1d_blocks = partial(levenshtein_1d_blocks, transpositions=True)


# TODO: should not consider the flag in string length when recursing?
def levenshtein_2d_blocks(string, transpositions=False, flag='\x00', inner_flag='\x01'):
    """
    Function returning the minimal set of longest Levenshtein distance <= 2
    blocking keys of target string. Note that this method is basically a one
    time recursion over the `levensthein_1d_blocks` scheme.

    Args:
        string (str): Target string.
        transpositions (bool, optional): Whether to support transpositions
            like with the Damerau-Levenshtein distance. Defaults to False.

    Returns:
        tuple: Resulting blocks.

    """

    blocks_1d = levenshtein_1d_blocks(string, transpositions=transpositions, flag=flag)
    blocks_2d = []

    for block in blocks_1d:
        blocks_2d.extend(levenshtein_1d_blocks(block, transpositions=transpositions, flag=inner_flag))

    return tuple(blocks_2d)
