# =============================================================================
# Fog MinHash LSH
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
import binascii
import math
from random import Random

from fog.lsh.utils import popcount

MAX_UINT32 = (2 ** 32) - 1
NEXT_PRIME = 4294967311


def crc32(x):
    return binascii.crc32(x.encode()) & 0xFFFFFFFF


class MinHash(object):

    def __init__(self, h=256, seed=None):
        # TODO: cheap_hashes
        # TODO: lsb

        rng = Random(seed)

        A = set()
        B = set()

        while len(A) < h:
            A.add(rng.randint(0, MAX_UINT32))
        while len(B) < h:
            B.add(rng.randint(0, MAX_UINT32))

        self.A = list(A)
        self.B = list(B)

        self.h = h

    def create_signature(self, sequence):
        A = self.A
        B = self.B

        if type(sequence) is str:
            tokens = set(ord(c) for c in sequence)
        else:
            tokens = set(crc32(token) for token in sequence)

        signature = [0] * self.h

        if len(tokens) == 0:
            return signature

        # TODO: numpy?
        for s in range(self.h):
            min_hash = MAX_UINT32

            for token in tokens:
                h = (A[s] * token + B[s]) % NEXT_PRIME

                if h < min_hash:
                    min_hash = h

            signature[s] = min_hash

        return signature

    def similarity(self, signatureA, signatureB):

        hamming = 0
        h = len(signatureA)

        for i in range(h):
            if signatureA[i] != signatureB[i]:
                hamming += 1

        return 1.0 - hamming / h


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

    def similarity(self, signatureA, signatureB):

        hamming = 0
        h = len(signatureA)

        for i in range(h):
            if signatureA[i] != signatureB[i]:
                hamming += 1

        return 1.0 - hamming / h


class LSBMinHash(object):

    def __init__(self, precision=8, seed=None):
        # TODO: weighted
        # TODO: cheap_hashes

        rng = Random(seed)

        h = precision * 64

        A = set()
        B = set()

        while len(A) < h:
            A.add(rng.randint(0, MAX_UINT32))
        while len(B) < h:
            B.add(rng.randint(0, MAX_UINT32))

        self.A = list(A)
        self.B = list(B)

        self.precision = precision

    def create_signature(self, sequence):
        A = self.A
        B = self.B

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

                for token in tokens:
                    h = (A[offset + i] * token + B[offset + i]) % NEXT_PRIME

                    if h < min_hash:
                        min_hash = h

                integer |= ((min_hash & 0x1) << i)

            signature[s] = integer

        return signature

    def similarity(self, signatureA, signatureB):

        hamming = 0
        L = len(signatureA)
        h = L * 64.0

        for i in range(L):
            hamming += popcount(signatureA[i] ^ signatureB[i])

        return 1.0 - 2.0 * hamming / h
