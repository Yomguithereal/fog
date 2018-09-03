# =============================================================================
# Fog Miscellaneaous Keys
# =============================================================================
#
# Miscellaneous set of key functions used for blocking and/or sorted
# neighborhood approaches.
#
# [References]:
# Christen, Peter. « A Survey of Indexing Techniques for Scalable Record
# Linkage and Deduplication ». IEEE Transactions on Knowledge and Data
# Engineering 24, no 9 (septembre 2012): 1537‑55.
# https://doi.org/10.1109/TKDE.2011.127.
#
# Knuth, D. 1997. The Art of Computer Programming. Sorting and Searching,
# 2d ed., vol. 3. Addison-Wesley, Upper Saddle River, NJ. p. 394
#
import math
from itertools import chain, combinations
from fog.tokenizers import ngrams

# Following Knuth's intuitions, sorting keys twice, once normally and once
# over the reversed strings, yields very good results when applying sorted
# neighborhood method over edit distances.
zig_zag = (None, lambda x: x[::-1])


# TODO: way to choose l instead in negative by number max of match
def ngram_keys(n, string, threshold=0.8):
    """
    Function returning n-gram keys for the given string. Useful for blocking.
    Note that this method is only suitable with small strings (a single name,
    for instance), else the number of combinations will explode and generate
    way too many keys.

    Args:
        n (number): Size of the grams.
        string (str): Target string.
        threshold (number, optional): Threshold controlling the number
            of grams that can be missing from two compared strings so they
            collide on at least one key. Defaults to 0.8.

    Yields:
        str: A single key.

    """
    k = len(string) - (n - 1)
    l = max(1, math.floor(k * threshold))

    grams = list(ngrams(n, string))

    yield ''.join(grams)

    s = k
    iterator = iter([])

    while s > l:
        s -= 1

        iterator = chain(iterator, combinations(grams, s))

    for g in iterator:
        yield ''.join(g)
