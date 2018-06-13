# =============================================================================
# Fog MinHash LSH
# =============================================================================
#
# Classes & functions related to the MinHash Local Sensitivity Hashing scheme.
#
# [Url]:
# https://en.wikipedia.org/wiki/MinHash
#
# [Reference]:
# Broder, Andrei Z. (1997), "On the resemblance and containment of documents",
# Compression and Complexity of Sequences: Proceedings, Positano,
# Amalfitan Coast, Salerno, Italy, June 11-13, 1997.
#
import binascii
from random import Random

from fog.lsh.utils import popcount

MAX_UINT32 = (2 ** 32) - 1
NEXT_PRIME = 4294967311


def crc32(x):
    return binascii.crc32(x.encode())


class LSBMinHash(object):

    def __init__(self, seed=None, precision=8):

        rng = Random(seed)

        N = precision * 64

        A = set()
        B = set()

        while len(A) < N:
            A.add(rng.randint(0, MAX_UINT32))
        while len(B) < N:
            B.add(rng.randint(0, MAX_UINT32))

        self.A = list(A)
        self.B = list(B)

        self.precision = precision

    def hash(self, tokens):
        A = self.A
        B = self.B

        crc32_set = set(crc32(token) for token in tokens)

        signature = [0] * self.precision

        if len(crc32_set) == 0:
            return signature

        for s in range(self.precision):
            integer = 0

            for i in range(64):
                min_hash = NEXT_PRIME

                for token in crc32_set:
                    h = (A[s * 64 + i] * token + B[s * 64 + i]) % NEXT_PRIME

                    if h < min_hash:
                        min_hash = h

                if min_hash & 0x1 > 0:
                    integer |= (1 << i)

            signature[s] = integer

        return signature

    def similarity(self, signatureA, signatureB):

        hamming = 0
        L = len(signatureA)
        N = L * 64.0

        for i in range(L):
            hamming += popcount(signatureA[i] ^ signatureB[i])

        return 1.0 - 2.0 * hamming / N
