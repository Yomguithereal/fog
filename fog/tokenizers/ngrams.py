# =============================================================================
# Fog Ngrams Tokenizers
# =============================================================================
#
# Functions related to n-grams.
#
from functools import partial


def ngrams(n, tokens):
    """
    Function returning an iterator over the given sequence's n-grams. The
    type of yielded n-grams will match the sequence's one.

    Args:
        n (number): size of the subsequences.
        tokens (iterable): token sequence, should support random access.

    Yields:
        tuple or string: A n-gram.

    """
    limit = len(tokens) - n + 1

    for i in range(limit):
        yield tokens[i:i + n]


bigrams = partial(ngrams, 2)
trigrams = partial(ngrams, 3)
quadrigrams = partial(ngrams, 4)
