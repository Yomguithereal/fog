# =============================================================================
# Fog Ngrams Tokenizers
# =============================================================================
#
# Functions returning iterators of n-grams.
#
from functools import partial


def ngrams(n, tokens):
    """
    Function returning an iterator of n-grams of the given sequence of tokens.

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
