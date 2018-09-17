# =============================================================================
# Fog Levensthein Keys
# =============================================================================
#
# Functions related to solving the Levenshtein & Damerau-Levenshtein <= 1/2
# problem efficiently by providing collision keys & blocks.
#
# [References]:
# Boytsov, Leonid. « Indexing Methods for Approximate Dictionary Searching:
# Comparative Analysis ». Journal of Experimental Algorithmics 16 (1 mai 2011).
# https://doi.org/10.1145/1963190.1963191.
#
# Doster. « Contextual Postprocessing System for Cooperation with a
# Multiple-Choice Character-Recognition System ». IEEE Transactions on
# Computers C-26, no 11 (novembre 1977): 1090‑1101.
# https://doi.org/10.1109/TC.1977.1674755.
#
# Knuth, D. 1997. The Art of Computer Programming. Sorting and Searching,
# 2d ed., vol. 3. Addison-Wesley, Upper Saddle River, NJ. p. 394
#
# Sutinen, Erkki, et Jorma Tarhio. « Filtration with q-samples in approximate
# string matching ». In Combinatorial Pattern Matching, 1075:50‑63. Berlin,
# Heidelberg: Springer Berlin Heidelberg, 1996.
# https://doi.org/10.1007/3-540-61258-0_4.
#
# Bast, Hannah, et Marjan Celikik. « Efficient Fuzzy Search in Large Text
# Collections ». ACM Transactions on Information Systems 31, no 2
# (1 mai 2013): 1‑59.
# https://doi.org/10.1145/2457465.2457470.
#
from functools import partial


# TODO: also try Mor-Fraenkel index for k = 1 using only deletions
# TODO: k-truncated from Efficient Fuzzy Search in Large Text Collections.pdf
# TODO: rename wildcard_neighborhood and rename package
def levenshtein_1d_keys(string, transpositions=False, flag='\x00'):
    """
    Function returning an iterator over Levenshtein 1D keys, being the series
    of keys colliding with other strings being at a Levenshtein distance of
    1 with the given string.

    This works by generating a set of collision keys such as two strings may
    only share a key if they have a Levenshtein distance <= 1.

    Note that the number of keys is proportional to the size of the string:
        - 1 key + n substition keys + (n + 2) addition keys, i.e. (2n + 3) keys
          for Levenshtein distance.
        - n - 1 keys for transpositions, i.e. (3n + 2) total keys
          for Damerau-Levenshtein distance.

    In the literature, this technique seems to be called generating the
    "wildcard neighborhood" of a string. It's quite efficient compared to
    traditional neighborhood methods because the number of keys is not
    dependent on the size of the alphabet since we use a wildcard to represent
    the substitutions/additions.

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
        # for B->A. So, in fact, substitution key and transposition keys will
        # match when required.

        # When some letters are doubled, we can skip some keys
        if i > 0 and string[i - 1] == string[i]:
            continue

        yield string[:i] + flag + string[i:]

    # Last addition
    yield string + flag


damerau_levenshtein_1d_keys = partial(levenshtein_1d_keys, transpositions=True)


# TODO: half-grams, easily parallelizable method
# TODO: include positional info + length info (get filtering refs in paper)
# TODO: no rolling to avoid generating too much keys
# TODO: test the deletion of middle char (more collisions, less keys)
# TODO: if even and transposing, if doubled letter, don't need to generate tr keys
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

    The intuition of this technique can be found in Knuth. Similar concepts can
    be found in Doster. This is also reminiscent of q-samples.

    This method works quite well because it's independent of the string's
    length and therefore implicitly incorporates the string's length into
    the generated keys.

    Indeed, this method minimizes the number of produced keys (the number
    is constant, contrary to n-grams, for instance) and minimizes the
    probability of two strings colliding.

    What's more, this method is exact and won't generate false negatives like
    n-grams would.

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
    if n % 2 == 0:

        first_half = flag + string[:h]
        second_half = string[h:] + flag

        # For transpositions, we swap once the middle characters
        if transpositions:

            first_transposed_half = flag + string[:h - 1] + second_half[0]
            second_transposed_half = first_half[-1] + string[h + 1:] + flag

            return (first_half, second_half, first_transposed_half, second_transposed_half)
        else:
            return (first_half, second_half)

    # String has odd length, we split twice
    h1 = h + 1

    first_half = flag + string[:h]
    second_half = string[h:] + flag
    first_half1 = flag + string[:h1]
    second_half1 = string[h1:] + flag

    return (first_half, second_half, first_half1, second_half1)


damerau_levenshtein_1d_blocks = partial(levenshtein_1d_blocks, transpositions=True)


# TODO: generalize to 3 and make a dynamic version
def levenshtein_2d_blocks(string, transpositions=False,
                          flag1='\x00', flag2='\x01', flag3='\x02'):
    """
    Function returning the minimal set of longest Levenshtein distance <= 2
    blocking keys of target string. Note that this method is basically a
    generalization of the `levensthein_1d_blocks` scheme.

    Args:
        string (str): Target string.
        transpositions (bool, optional): Whether to support transpositions
            like with the Damerau-Levenshtein distance. Defaults to False.

    Returns:
        tuple: Resulting blocks.

    """

    n = len(string)
    q = n % 3

    if q == 0:
        h = n // 3

        basic = (
            flag1 + string[:h],
            flag2 + string[h:h * 2],
            flag3 + string[h * 2:]
        )

        if transpositions:
            h1 = h - 1

            return basic + (
                flag1 + string[:h1] + string[h],
                flag2 + string[h1] + string[h + 1:h * 2],
                flag3 + string[h * 2 - 1] + string[h * 2 + 1:]
            )

        return basic

    elif q == 2:
        h1 = n // 3
        h = h1 + 1

        return (
            flag1 + string[:h],
            flag2 + string[h:h * 2],
            flag3 + string[h * 2:],

            flag1 + string[:h1],
            flag2 + string[h1:h + h1],
            flag3 + string[h + h1:],

            flag2 + string[h:h + h1]
        )

    elif q == 1:
        h1 = n // 3
        h = h1 + 1

        return (
            flag1 + string[:h],
            flag2 + string[h:h + h1],
            flag3 + string[h + h1:],

            flag1 + string[:h1],
            flag2 + string[h1:h1 + h],

            flag2 + string[h1:h1 * 2],
            flag3 + string[h1 * 2:]
        )


damerau_levenshtein_2d_blocks = partial(levenshtein_2d_blocks, transpositions=True)
