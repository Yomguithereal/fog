# =============================================================================
# Fog Jaccard Similarity Unit Tests
# =============================================================================
from pytest import approx
from collections import Counter
from fog.metrics import weighted_jaccard_similarity

BASIC_TESTS = [
    ({}, {}, 0.0),
    ({}, {0: 3}, 0.0),
    ({0: 2}, {0: 2}, 1.0),
    ({0: 2}, {0: 4}, 0.5),
    (Counter('contexte'), Counter('contact'), 0.5),
    (Counter('contexte'), Counter('contactant'), 0.385)
]


class TestWeightedJaccardSimilarity(object):
    def test_basics(self):
        for A, B, similarity in BASIC_TESTS:
            assert weighted_jaccard_similarity(A, B) == approx(similarity, 1e-2)
