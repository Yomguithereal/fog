# =============================================================================
# Fog MinHash
# =============================================================================
#
# Classes & functions related to the MinHash Local Sensitivity Hashing scheme.
#
# [Urls]:
# https://en.wikipedia.org/wiki/MinHash
# https://arxiv.org/abs/1706.05698
#
# [Reference]:
# Broder, Andrei Z. (1997), "On the resemblance and containment of documents",
# Compression and Complexity of Sequences: Proceedings, Positano,
# Amalfitan Coast, Salerno, Italy, June 11-13, 1997.
#
# Ertl, Otmar. « SuperMinHash - A New Minwise Hashing Algorithm for Jaccard
# Similarity Estimation ». arXiv:1706.05698 [cs], 18 juin 2017.
#
import math
from random import Random

try:
    import numpy as np
except:
    np = None

from fog.lsh.utils import crc32, popcount64

MAX_UINT32 = (2 ** 32) - 1
NEXT_PRIME = 4294967311


def minhash_similarity(A, B):
    hamming = 0
    h = len(A)

    for i in range(h):
        if A[i] != B[i]:
            hamming += 1

    return 1.0 - hamming / h


def lsb_minhash_similarity(A, B):
    hamming = 0
    L = len(A)
    h = L * 64.0

    for i in range(L):
        hamming += popcount64(A[i] ^ B[i])

    return 1.0 - 2.0 * hamming / h


class MinHash(object):

    __slots__ = ('A', 'B', 'params', 'h', 'numpy')

    def __init__(self, h=256, seed=None, use_numpy=False):

        # Properties
        self.A = None
        self.B = None
        self.params = None

        if use_numpy:
            assert np is not None, 'numpy is not installed'

            np.random.seed(seed)

            self.A = np.random.randint(1, MAX_UINT32, size=h, dtype='uint32')
            self.B = np.random.randint(0, MAX_UINT32, size=h, dtype='uint32')

            self.numpy = True
        else:

            rng = Random(seed)

            params = set()

            while len(params) < h:
                params.add((
                    rng.randint(1, MAX_UINT32),
                    rng.randint(0, MAX_UINT32)
                ))

            self.params = list(params)
            self.numpy = False

        self.h = h

    def create_signature(self, sequence):

        if type(sequence) is str:
            tokens = set(ord(c) for c in sequence)
        else:
            tokens = set(crc32(token) for token in sequence)

        # Using numpy
        if self.numpy:

            if len(tokens) == 0:
                return np.zeros(self.h, dtype=np.uint32)

            signature = np.repeat(list(tokens), self.h).astype(np.uint32, copy=False)
            signature.shape = (len(tokens), self.h)

            # Universal hash
            signature *= self.A
            signature += self.B
            signature %= NEXT_PRIME

            return signature.min(axis=0)

        # Standard routine
        params = self.params
        signature = [0] * self.h

        if len(tokens) == 0:
            return signature

        for s in range(self.h):
            min_hash = MAX_UINT32
            a, b = params[s]

            for token in tokens:
                h = (a * token + b) % NEXT_PRIME

                if h < min_hash:
                    min_hash = h

            signature[s] = min_hash

        return signature


class SuperMinHash(object):

    def __init__(self, h=256):
        self.h = h
        self.rng = Random()

    def create_signature(self, sequence):

        if type(sequence) is str:
            tokens = set(ord(c) for c in sequence)
        else:
            tokens = set(crc32(token) for token in sequence)

        m = self.h
        rng = self.rng

        h = [m + 1] * m
        p = [0] * m
        q = [-1] * m
        b = [0] * m

        b[-1] = m

        a = m - 1

        for i, token in enumerate(tokens):
            rng.seed(token)
            j = 0

            while j <= a:
                r = rng.random()
                k = j + math.floor(r * (m - j))

                if q[j] != i:
                    q[j] = i
                    p[j] = j

                if q[k] != i:
                    q[k] = i
                    p[k] = k

                tmp = p[j]
                p[j] = p[k]
                p[k] = tmp

                if r + j < h[p[j]]:
                    j2 = min(math.floor(h[p[j]]), m - 1)
                    h[p[j]] = r + j

                    if j < j2:
                        b[j2] -= 1
                        b[j] += 1

                        while b[a] == 0:
                            a -= 1

                j += 1

        return [int(i) for i in h]


class LSBMinHash(object):

    def __init__(self, precision=8, seed=None):
        # TODO: cheap_hashes

        rng = Random(seed)

        h = precision * 64

        params = set()

        while len(params) < h:
            params.add((
                rng.randint(1, MAX_UINT32),
                rng.randint(0, MAX_UINT32)
            ))

        self.params = list(params)
        self.precision = precision

    def create_signature(self, sequence):
        params = self.params

        if type(sequence) is str:
            tokens = set(ord(c) for c in sequence)
        else:
            tokens = set(crc32(token) for token in sequence)

        signature = [0] * self.precision

        if len(tokens) == 0:
            return signature

        # TODO: numpy?
        for s in range(self.precision):
            integer = 0
            offset = s * 64

            for i in range(64):
                min_hash = MAX_UINT32
                a, b = params[offset + i]

                for token in tokens:
                    h = (a * token + b) % NEXT_PRIME

                    if h < min_hash:
                        min_hash = h

                integer |= ((min_hash & 0x1) << i)

            signature[s] = integer

        return signature
