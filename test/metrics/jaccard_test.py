# =============================================================================
# Fog Jaccard Similarity Unit Tests
# =============================================================================
from pytest import approx
from collections import Counter
from fog.metrics import jaccard_similarity, weighted_jaccard_similarity

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

WEIGHTED_TESTS = [
    ({}, {}, 0.0),
    ({}, {0: 3}, 0.0),
    ({0: 2}, {0: 2}, 1.0),
    ({0: 2}, {0: 4}, 0.5),
    (Counter('contexte'), Counter('contact'), 0.5),
    (Counter('contexte'), Counter('contactant'), 0.385)
]


class TestJaccardSimilarity(object):
    def test_basics(self):
        for A, B, similarity in TESTS:
            assert jaccard_similarity(A, B) == similarity


class TestWeightedJaccardSimilarity(object):
    def test_basics(self):
        for A, B, similarity in WEIGHTED_TESTS:
            assert weighted_jaccard_similarity(A, B) == approx(similarity, 1e-2)
