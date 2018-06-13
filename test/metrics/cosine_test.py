# =============================================================================
# Fog Cosine Similarity Unit Tests
# =============================================================================
import math
from pytest import approx
from fog.metrics import sparse_cosine_similarity, sparse_dotproduct

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


def norm(S):
    return math.sqrt(sum(map(lambda x: x * x, S.values())))


class TestSparseCosineSimilarity(object):
    def test_basics(self):
        for A, B, similarity in BASIC_TESTS:
            assert sparse_cosine_similarity(A, B) == approx(similarity, abs=1e-2)

    def test_dotproduct(self):
        for A, B, similarity in BASIC_TESTS:
            dotproduct = sparse_dotproduct(A, B)
            A_norm = norm(A)
            B_norm = norm(B)

            cosine = 0.0

            if A_norm != 0 and B_norm != 0:
                cosine = dotproduct / (A_norm * B_norm)

            assert cosine == approx(similarity, abs=1e-2)
