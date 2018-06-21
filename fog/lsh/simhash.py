# =============================================================================
# Fog Simhash
# =============================================================================
#
# Classes & functions related to the Simhash Local Sensitivity Hashing scheme.
#
# [Urls]:
# https://en.wikipedia.org/wiki/SimHash
#
# [Reference]:
# Charikar, Moses S. (2002), "Similarity estimation techniques from rounding
# algorithms", Proceedings of the 34th Annual ACM Symposium on Theory of
# Computing.
#
import hashlib

from fog.lsh.utils import popcount


def simhash(tokens):
    histogram = [0] * 128

    for token in tokens:
        h = hashlib.md5()
        h.update(token.encode())
        h = int(h.hexdigest(), 16)

        for i in range(128):
            if (h >> i) & 1 == 1:
                histogram[i] += 1
            else:
                histogram[i] -= 1

    signature = 0

    for i in range(128):
        if histogram[i] > 0:
            signature |= (1 << i)

    return signature


def simhash_distance(A, B):
    return popcount(A ^ B) / 128


def simhash_similarity(A, B):
    return 1.0 - popcount(A ^ B) / 128


if __name__ == '__main__':
    from fog.metrics import sparse_cosine_similarity
    from fog.tokenizers import ngrams
    from collections import Counter

    TESTS = [
        (
            'the cat sat on the mat',
            'the cat sat on a mat'
        ),
        (
            'whatever floats your goat',
            'whatever floats your moat'
        ),
        (
            'aaabbc',
            'zzzyyx'
        )
    ]

    for s1, s2 in TESTS:
        print(s1)
        print(s2)
        s1 = list(ngrams(2, s1))
        s2 = list(ngrams(2, s2))

        sm1 = simhash(s1)
        sm2 = simhash(s2)

        print(sm1, sm2)
        print(sparse_cosine_similarity(Counter(s1), Counter(s2)))
        print(simhash_similarity(sm1, sm2))
        print()
