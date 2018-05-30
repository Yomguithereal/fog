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

    def test_key(self):
        tests = []

        for test in BASIC_TESTS:
            tests.append((
                {k: {'weight': v} for k, v in test[0].items()},
                {k: {'weight': v} for k, v in test[1].items()},
                test[2]
            ))

        for A, B, similarity in tests:
            assert weighted_jaccard_similarity(A, B, key=lambda x: x['weight']) == approx(similarity, 1e-2)
