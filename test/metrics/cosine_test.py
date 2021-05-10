# =============================================================================
# Fog Cosine Similarity Unit Tests
# =============================================================================
import math
from pytest import approx
from fog.metrics import (
    cosine_similarity,
    sparse_cosine_similarity,
    sparse_dot_product,
    sparse_binary_cosine_similarity,
    sparse_norm,
    sparse_normalize,
    binary_cosine_similarity
)

BASIC_TESTS = [
    ({}, {}, 0.0),
    ({}, {0: 3}, 0.0),
    ({0: 2}, {0: 2}, 1.0),
    ({0: 2}, {0: 4}, 1.0),
    ({0: 1, 1: 3}, {0: 4, 1: 5}, 0.94),
    ({0: 1, 1: 3, 2: 5}, {0: 2, 1: 1, 2: 4}, 0.92),
    ({0: 23, 3: 12}, {0: 45, 3: 9}, 0.96),
    ({0: 34, 2: 12, 3: 4}, {0: 45, 1: 12, 3: 4}, 0.91)
]

SEQUENCE_TESTS = [
    ('', '', 0.0),
    ('test', '', 0.0),
    ('', 'test', 0.0),
    ('the cat sat on the mat', 'the cat sat on a mat', 0.97),
    ('whatever floats your goat', 'whatever floats your moat', 0.98),
    ('aaabbbc', 'zzzyyx', 0.0)
]

SPARSE_BINARY_TESTS = [
    ({'A', 'B', 'C', 'D', 'E'}, {'F', 'B', 'C', 'D', 'E'}, 0.8)
]

BINARY_TESTS = [
    ('ABCDEEEDECCCDEA', 'FBBBCDEDDDED', 0.8)
]


class TestSparseCosineSimilarity(object):
    def test_basics(self):
        for A, B, similarity in BASIC_TESTS:
            assert sparse_cosine_similarity(A, B) == approx(similarity, abs=1e-2)

    def test_string(self):
        for A, B, similarity in SEQUENCE_TESTS:
            assert cosine_similarity(A, B) == approx(similarity, abs=1e-2)

    def test_dotproduct(self):
        for A, B, similarity in BASIC_TESTS:
            dotproduct = sparse_dot_product(A, B)
            A_norm = sparse_norm(A)
            B_norm = sparse_norm(B)

            cosine = 0.0

            if A_norm != 0 and B_norm != 0:
                cosine = dotproduct / (A_norm * B_norm)

            assert cosine == approx(similarity, abs=1e-2)

    def test_binary(self):
        for A, B, similarity in SPARSE_BINARY_TESTS:
            assert sparse_binary_cosine_similarity(A, B) == approx(similarity)

        for A, B, similarity in BINARY_TESTS:
            assert binary_cosine_similarity(A, B) == approx(similarity)

    def test_sparse_normalize(self):
        vector = {'A': 34, 'B': 78, 'C': -16}
        unit = sparse_normalize(vector)

        for w in unit.values():
            assert w >= -1.0 and w <= 1.0

        assert unit == approx({
            'A': 0.39270291779351885,
            'B': 0.900906693761602,
            'C': -0.184801373079303
        })
