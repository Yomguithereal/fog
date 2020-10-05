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

from fog.lsh.utils import is_power_of_two, popcount

# TODO: reimplement soundly by following:
# https://github.com/reubano/changanya/blob/master/changanya/simhash.py
# Note: Simhash clustering methods I could find are two slow (mozilla's one)
# and even Hamming space indexation ones.
# I should try again to use the same lsh method used by minhash to see if it
# yields similar results

# TODO: reference papers
# https://github.com/leonsim/simhash/blob/master/simhash/__init__.py#L116-L208
# https://github.com/scrapinghub/python-simhash
# http://www.wwwconference.org/www2007/papers/paper215.pdf
# https://github.com/seomoz/simhash-cpp/tree/e7aacb1642f406ff0815cf402e909d2002473812
# https://ir.library.dc-uoit.ca/bitstream/10155/475/1/Rodriguez%20Reina_Ernesto.pdf


def simhash(tokens, f=128):
    assert f <= 512 and not is_power_of_two(f), 'fog.lsh.simhash: f should be a power of 2 <= 512'

    histogram = [0] * f

    l = f >> 2
    hash_func = hashlib.md5

    if f == 256:
        hash_func = hashlib.sha256

    elif f == 512:
        hash_func = hashlib.sha512

    for token in tokens:
        h = hash_func()
        h.update(token.encode())
        h = int(h.hexdigest()[0:l], 16)

        for i in range(f):
            r = ((h >> i) & 1)
            histogram[i] += r - (r ^ 1)

    signature = 0

    for i in range(f):
        if histogram[i] > 0:
            signature |= (1 << i)

    return signature


def simhash_distance(A, B, f=128):
    return popcount(A ^ B) / f


def simhash_similarity(A, B, f=128):
    return 1.0 - popcount(A ^ B) / f


if __name__ == '__main__':
    from fog.metrics import cosine_similarity
    from fog.tokenizers import ngrams

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
            'hello darkness my old friend',
            'goodbye darkness my old friends'
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

        for i in [32, 64, 128, 256, 512]:
            sm1 = simhash(s1, f=i)
            sm2 = simhash(s2, f=i)

            print(i)
            print(sm1, sm2)
            print(cosine_similarity(s1, s2))
            print(simhash_similarity(sm1, sm2, f=i))
            print()
