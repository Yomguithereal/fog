# =============================================================================
# Fog Cosine Similarity Unit Tests
# =============================================================================
from pytest import approx
from fog.metrics import sparse_cosine_similarity

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


class TestSparseCosineSimilarity(object):
    def test_basics(self):
        for A, B, similarity in BASIC_TESTS:
            assert sparse_cosine_similarity(A, B) == approx(similarity, 1e-2)

    def test_key(self):
        tests = []

        for test in BASIC_TESTS:
            tests.append((
                {k: {'weight': v} for k, v in test[0].items()},
                {k: {'weight': v} for k, v in test[1].items()},
                test[2]
            ))

        for A, B, similarity in tests:
            assert sparse_cosine_similarity(A, B, key=lambda x: x['weight']) == approx(similarity, 1e-2)
