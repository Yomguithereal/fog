# =============================================================================
# Fog MinHash LSH Unit Tests
# =============================================================================
import numpy as np
from pytest import approx
from fog.lsh import MinHash, LSBMinHash, SuperMinHash

TESTS = [
    ('abc', '', 0),
    ('', 'abc', 0),
    ('', '', 1),
    ('abc', 'abc', 1),
    ('abc', 'xyz', 0),
    ('night', 'nacht', 3 / 7),
    ('context', 'contact', 4 / 7),
    ('ht', 'nacht', 2 / 5)
]


class TestLSBMinHash(object):
    def test_basics(self):
        m = MinHash(512, seed=123)

        for A, B, j in TESTS:
            sA = m.create_signature(A)
            sB = m.create_signature(B)

            assert m.similarity(sA, sB) == approx(j, abs=1e-1)

    def test_numpy(self):
        m = MinHash(512, seed=123, use_numpy=True)

        for A, B, j in TESTS:
            sA = m.create_signature(A)
            sB = m.create_signature(B)

            assert sA.shape == (512, )
            assert sA.dtype == np.uint32

            assert m.similarity(sA, sB) == approx(j, abs=1e-1)

    def test_lsb(self):
        m = LSBMinHash(precision=16, seed=123)

        for A, B, j in TESTS:
            sA = m.create_signature(A)
            sB = m.create_signature(B)

            assert m.similarity(sA, sB) == approx(j, abs=1e-1)

    def test_super_minhash(self):
        m = SuperMinHash(512)

        for A, B, j in TESTS:
            sA = m.create_signature(A)
            sB = m.create_signature(B)

            assert m.similarity(sA, sB) == approx(j, abs=1e-1)
